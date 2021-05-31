from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import json
from django.contrib import messages
import datetime
from login.models import Rawmaterial,Rawmaterialchild
from supplier.models import Materialtransfer,Materialpurchase
from django.db.models import Count, Max


def transfertosizing(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				 return render(request, 'dashboard/transfertosizing.html')

def gettransferview(request,fromdate,todate):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				cursor = connection.cursor()
				cursor.execute("SELECT `transferno`,`transferdate`,c.company sizingname,address,contact FROM(SELECT DISTINCT `transferno`,`transferdate`,`sizing` FROM supplier_materialtransfer where `deleted`=0 AND `transferdate` BETWEEN %s and %s) a  INNER JOIN login_sizing c  on a.sizing=c.id ORDER BY transferno DESC,transferdate DESC",[fromdate,todate])
				row = cursor.fetchall()
				#data= serialize("json",row)
				json_data = []
				for obj in row:
								 json_data.append({"transferno" : obj[0], "transferdate" : obj[1],"sizingname": obj[2],"sizingaddress": obj[3],"sizingcontact": obj[4]})

				return JsonResponse(json_data, safe=False)


def getmaterial(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				cursor = connection.cursor()
				cursor.execute("SELECT b.`id`, `materialchild`, `materialname` FROM login_rawmaterial a inner join  login_rawmaterialchild b on a.id=b.fid order by fid asc")
				row = cursor.fetchall()
				#data= serialize("json",row)
				json_data = []
				for obj in row:
								 json_data.append({"fid" : obj[0], "materialchild" : obj[1],"materialname": obj[2]})

				return JsonResponse(json_data, safe=False)

def getreceiptno(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				date = datetime.datetime.now()
				if date.month>=4:
					 from_date=str(date.year)+'-04-01'
					 to_date=str(date.year+1)+'-03-31'
				else:
					 from_date=str(date.year-1)+'-04-01'
					 to_date=str(date.year)+'-03-31'

				Material = Materialtransfer.objects.filter(transferdate__range=[from_date, to_date]).aggregate(transferno=Max('transferno'))
		
				return HttpResponse(json.dumps(Material))


def addmaterialtransfer(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 transferno = data['transferno']
						 transferdate = data['transferdate']
						 if int(data['status'])==0:
								d=transferdate.split('-')
								date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
								if date.month>=4:
									from_date=str(date.year)+'-04-01'
									to_date=str(date.year+1)+'-03-31'
								else:
									from_date=str(date.year-1)+'-04-01'
									to_date=str(date.year)+'-03-31'
								t_no = Materialtransfer.objects.filter(transferdate__range=[from_date, to_date]).aggregate(transferno=Max('transferno'))['transferno']
								t_no1=0 if t_no is None else t_no
								tmax=t_no1+1
						 else:
								tmax = transferno
						
						 sizing=data['sizing']
						 materialtype=data['materialtype']
						 count=data['count'] if data['count']!='' else 0
						 grossweight=data['grossweight'] if data['grossweight']!='' else 0
						 netweight=data['netweight'] if data['netweight']!='' else 0
						 bags=data['bags'] if data['bags']!='' else 0;
						 cones=data['cones'] if data['cones']!='' else 0;
						 tip=data['tip']
						 colorshade=data['colorshade']
						 form=Materialtransfer.objects.create(transferno=tmax,transferdate=transferdate,sizing=sizing,material=materialtype,count=count,gross_weight=grossweight,net_weight=netweight,no_of_bags=bags,number_of_cones=cones,user=request.user.id,color_shadeandnumber=colorshade)
						 fid=Materialtransfer.objects.filter(user=request.user.id).last().pk
						 response = "success"
						 return JsonResponse({"tno":tmax,"transferdate":transferdate}, status=201)

def updatematerialtransfer(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 transferno = data['transferno']
						 transferdate = data['transferdate']
						 idc = data['idc']
						 tmax = transferno
						 sizing=data['sizing']
						 materialtype=data['materialtype']
						 count=data['count'] if data['count']!='' else 0
						 grossweight=data['grossweight'] if data['grossweight']!='' else 0
						 netweight=data['netweight'] if data['netweight']!='' else 0
						 bags=data['bags'] if data['bags']!='' else 0;
						 cones=data['cones'] if data['cones']!='' else 0;
						 tip=data['tip']
						 colorshade=data['colorshade']
						 form=Materialtransfer.objects.filter(id=idc).update(sizing=sizing,material=materialtype,count=count,gross_weight=grossweight,net_weight=netweight,no_of_bags=bags,number_of_cones=cones,user=request.user.id,color_shadeandnumber=colorshade)
						 response = "success"
						 return JsonResponse({"tno":tmax,"transferdate":transferdate}, status=201)             

def getmaterialtransfer(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 transferno = data['transferno']
						 transferdate = data['transferdate']
						 deleted = False
						 cursor = connection.cursor()
						 cursor.execute("SELECT a.`id`,`count`, `gross_weight`, `net_weight`, `no_of_bags`, `number_of_cones`,`materialchild` FROM supplier_materialtransfer a INNER JOIN login_rawmaterialchild b on a.material=b.id where transferno=%s and transferdate=%s and deleted=%s",[transferno,transferdate,deleted])
						 row = cursor.fetchall()
				#data= serialize("json",row)
						 json_data = []
						 for obj in row:
									json_data.append({"fid" : obj[0], "count" : obj[1],"gross_weight": obj[2],"net_weight":obj[3],"no_of_bags":obj[4],"number_of_cones":obj[5],"materialtype":obj[6]})

						 return JsonResponse(json_data, safe=False)                     

def deletematerialtransfer(request, id):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				Materialt = Materialtransfer.objects.filter(id=id).update(deleted=True)
				response = "success"
				return JsonResponse({"msg":response}, status=201)

def editmaterialtransfer(request, id):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				Material = Materialtransfer.objects.filter(id=id) 
				data = serialize("json", Material, fields=('id', 'transferno', 'transferdate','sizing', 'material', 'count', 'gross_weight', 'net_weight', 'no_of_bags', 'number_of_cones', 'color_shadeandnumber'))
				return HttpResponse(data)       


def getmaterialtransfermodel(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 transferno = data['transferno']
						 transferdate = data['transferdate']
						 deleted = False
						 cursor = connection.cursor()
						 cursor.execute("SELECT DISTINCT `sizing`  FROM supplier_materialtransfer a  where transferno=%s and transferdate=%s and deleted=%s",[transferno,transferdate,deleted])
						 row = cursor.fetchall()
				#data= serialize("json",row)
						 json_data = []
						 for obj in row:
									json_data.append({"sizing" : obj[0]})
						 return JsonResponse(json_data, safe=False)

def deletematerialtransfermodel(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 transferno = data['transferno']
						 transferdate = data['transferdate']
						 Materialt = Materialtransfer.objects.filter(transferno=transferno,transferdate=transferdate).update(deleted=True)
						 response = "success"
						 return JsonResponse({"msg":response}, status=201) 

#----------------------------------------------------------------------------------------
def purchaseentry(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				 return render(request, 'dashboard/purchaseentry.html')

def getpurchaseview(request,fromdate,todate):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				cursor = connection.cursor()
				cursor.execute("SELECT `purchaseno`,`purchasedate`,b.company suppliername,address,contact FROM(SELECT DISTINCT `purchaseno`,`purchasedate`,`supplier` FROM supplier_materialpurchase where `deleted`=0 AND `purchasedate` BETWEEN %s and %s) a INNER JOIN login_supplier b on a.`supplier`=b.id    ORDER BY purchaseno DESC,purchasedate DESC",[fromdate,todate])
				row = cursor.fetchall()
				#data= serialize("json",row)
				json_data = []
				for obj in row:
								 json_data.append({"purchaseno" : obj[0], "purchasedate" : obj[1],"suppliername": obj[2],"supplieraddress": obj[3],"suppliercontact": obj[4]})

				return JsonResponse(json_data, safe=False)


def getmaterialpurchase(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				cursor = connection.cursor()
				cursor.execute("SELECT b.`id`, `materialchild`, `materialname` FROM login_rawmaterial a inner join  login_rawmaterialchild b on a.id=b.fid order by fid asc")
				row = cursor.fetchall()
				#data= serialize("json",row)
				json_data = []
				for obj in row:
								 json_data.append({"fid" : obj[0], "materialchild" : obj[1],"materialname": obj[2]})

				return JsonResponse(json_data, safe=False)

def getpurchaseno(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				date = datetime.datetime.now()
				if date.month>=4:
					 from_date=str(date.year)+'-04-01'
					 to_date=str(date.year+1)+'-03-31'
				else:
					 from_date=str(date.year-1)+'-04-01'
					 to_date=str(date.year)+'-03-31'

				Material = Materialpurchase.objects.filter(purchasedate__range=[from_date, to_date]).aggregate(purchaseno=Max('purchaseno'))
		
				return HttpResponse(json.dumps(Material))


def addmaterialpurchase(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 purchaseno = data['purchaseno']
						 purchasedate = data['purchasedate']
						 if int(data['status'])==0:
								d=purchasedate.split('-')
								date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
								if date.month>=4:
									from_date=str(date.year)+'-04-01'
									to_date=str(date.year+1)+'-03-31'
								else:
									from_date=str(date.year-1)+'-04-01'
									to_date=str(date.year)+'-03-31'
								t_no = Materialpurchase.objects.filter(purchasedate__range=[from_date, to_date]).aggregate(purchaseno=Max('purchaseno'))['purchaseno']
								t_no1=0 if t_no is None else t_no
								tmax=t_no1+1
						 else:
								tmax = purchaseno
						 supplier = data['supplier']
						 materialtype=data['materialtype']
						 count=data['count'] if data['count']!='' else 0
						 grossweight=data['grossweight'] if data['grossweight']!='' else 0
						 netweight=data['netweight'] if data['netweight']!='' else 0
						 bags=data['bags'] if data['bags']!='' else 0;
						 cones=data['cones'] if data['cones']!='' else 0;
						 tip=data['tip']
						 colorshade=data['colorshade']
						 form=Materialpurchase.objects.create(purchaseno=tmax,purchasedate=purchasedate,supplier=supplier,material=materialtype,count=count,gross_weight=grossweight,net_weight=netweight,no_of_bags=bags,number_of_cones=cones,user=request.user.id,color_shadeandnumber=colorshade)
						 fid=Materialpurchase.objects.filter(user=request.user.id).last().pk
						 response = "success"
						 return JsonResponse({"tno":tmax,"purchasedate":purchasedate}, status=201)

def updatematerialpurchase(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 purchaseno = data['purchaseno']
						 purchasedate = data['purchasedate']
						 idc = data['idc']
						 tmax = purchaseno
						 supplier = data['supplier']
						 materialtype=data['materialtype']
						 count=data['count'] if data['count']!='' else 0
						 grossweight=data['grossweight'] if data['grossweight']!='' else 0
						 netweight=data['netweight'] if data['netweight']!='' else 0
						 bags=data['bags'] if data['bags']!='' else 0
						 cones=data['cones'] if data['cones']!='' else 0
						 tip=data['tip']
						 colorshade=data['colorshade']
						 form=Materialpurchase.objects.filter(id=idc).update(supplier=supplier,material=materialtype,count=count,gross_weight=grossweight,net_weight=netweight,no_of_bags=bags,number_of_cones=cones,user=request.user.id,color_shadeandnumber=colorshade)
						 response = "success"
						 return JsonResponse({"tno":tmax,"purchasedate":purchasedate}, status=201)             

def getmaterialpurchase(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 purchaseno = data['purchaseno']
						 purchasedate = data['purchasedate']
						 deleted = False
						 cursor = connection.cursor()
						 cursor.execute("SELECT a.`id`,`count`, `gross_weight`, `net_weight`, `no_of_bags`, `number_of_cones`,`materialchild` FROM supplier_materialpurchase a INNER JOIN login_rawmaterialchild b on a.material=b.id where purchaseno=%s and purchasedate=%s and deleted=%s",[purchaseno,purchasedate,deleted])
						 row = cursor.fetchall()
				#data= serialize("json",row)
						 json_data = []
						 for obj in row:
									json_data.append({"fid" : obj[0], "count" : obj[1],"gross_weight": obj[2],"net_weight":obj[3],"no_of_bags":obj[4],"number_of_cones":obj[5],"materialtype":obj[6]})

						 return JsonResponse(json_data, safe=False)                     

def deletematerialpurchase(request, id):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				Materialt = Materialpurchase.objects.filter(id=id).update(deleted=True)
				response = "success"
				return JsonResponse({"msg":response}, status=201)

def editmaterialpurchase(request, id):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				Material = Materialpurchase.objects.filter(id=id) 
				data = serialize("json", Material, fields=('id', 'purchaseno', 'purchasedate', 'supplier',  'material', 'count', 'gross_weight', 'net_weight', 'no_of_bags', 'number_of_cones', 'color_shadeandnumber'))
				return HttpResponse(data)       


def getmaterialpurchasemodel(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 purchaseno = data['purchaseno']
						 purchasedate = data['purchasedate']
						 deleted = False
						 cursor = connection.cursor()
						 cursor.execute("SELECT DISTINCT `supplier`  FROM supplier_materialpurchase a  where purchaseno=%s and purchasedate=%s and deleted=%s",[purchaseno,purchasedate,deleted])
						 row = cursor.fetchall()
				#data= serialize("json",row)
						 json_data = []
						 for obj in row:
									json_data.append({"supplier" : obj[0]})
						 return JsonResponse(json_data, safe=False)

def deletematerialpurchasemodel(request):
		if not request.user.is_authenticated:
				return redirect('login')
		else:
				if request.method == 'POST':
						 data = json.loads(request.body)

						 purchaseno = data['purchaseno']
						 purchasedate = data['purchasedate']
						 Materialt = Materialpurchase.objects.filter(purchaseno=purchaseno,purchasedate=purchasedate).update(deleted=True)
						 response = "success"
						 return JsonResponse({"msg":response}, status=201) 
