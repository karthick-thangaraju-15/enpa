from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.core.serializers import serialize
from login.form import UserForm,SupplierForm,SizingForm,ContractorForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .models import Supplier,Sizing,Contractor,District,Factorymaster,Loomentry,Supplierbankdetails,Contractorbankdetails,Sizingbankdetails
import json
from django.contrib import messages
from django.db.models import Count, Max

def index(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 return render(request, 'dashboard/index.html')

def getmaster(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 sid      = Supplier.objects.aggregate(scount=Count('id'))['scount']
		 sizingid = Sizing.objects.aggregate(sizingcount=Count('id'))['sizingcount']
		 contractorid = Contractor.objects.aggregate(Contractorcount=Count('id'))['Contractorcount']

		 result = { 'supplier': sid, 'sizings': sizingid, 'contractors':contractorid }
		
		 return HttpResponse(json.dumps(result,indent=4, separators=(',', ': ')))	

def districtget(request, state):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 DistrictS = District.objects.filter(State__istartswith=state[0:4])  
		 data = serialize("json", DistrictS, fields=('District'))
		 return HttpResponse(data)		
#supplier details--------------------------------------------------------
def supplier(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 return render(request, 'dashboard/supplier.html')

def getsupplier(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Suppliers = Supplier.objects.all()  
		data = serialize("json", Suppliers, fields=('id','company', 'name', 'contact', 'email', 'address', 'taluk', 'district', 'state', 'pincode', 'zone','gstno'))
		return HttpResponse(data)

def deletesupplier(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Suppliers = Supplier.objects.filter(id=id)
		Suppliers.delete()
		Suppliersbank = Supplierbankdetails.objects.filter(fid=id)
		Suppliersbank.delete()  
		response = "success"
		return JsonResponse({"msg":response}, status=201)

def editsupplier(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Suppliers = Supplier.objects.filter(id=id)  
		data = serialize("json", Suppliers, fields=('id','company', 'name', 'contact', 'email', 'address', 'taluk', 'district', 'state', 'pincode', 'zone','gstno'))
		return HttpResponse(data)

def editsupplierbank(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Suppliersbank = Supplierbankdetails.objects.filter(fid=id) 
		data = serialize("json", Suppliersbank, fields=('id', 'bankname', 'accountno', 'ifsccode'))
		return HttpResponse(data)						

def addsupplier(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		data={}
		if request.method == 'POST':
			 data = json.loads(request.body)
			 name = data['name']
			 company = data['company']
			 email = data['email']
			 contact = data['contact']
			 address = data['address']
			 taluk = data['taluk']
			 district = data['district']
			 state = data['state']
			 pincode = data['pincode']
			 zone = data['zone']
			 gstno = data['gstno']
			 form=Supplier.objects.create(name=name,company=company,contact=contact,email=email,address=address,taluk=taluk,district=district,state=state,pincode=pincode,zone=zone,gstno=gstno)
			 fid=Supplier.objects.filter(contact=contact).last().pk
			 count=len(data['bname'])
			 for x in range(count):
					bname=data['bname'][x]
					acno=data['acno'][x]
					ifsc=data['ifsc'][x]
					form1=Supplierbankdetails.objects.create(fid=fid,bankname=bname,accountno=acno,ifsccode=ifsc)

			 response = "success"
			 return JsonResponse({"msg":response}, status=201)
			 
		else:			
			 data['fail']="false"
			 return HttpResponse(data)

def updatesupplier(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		data={}
		if request.method == 'POST':
			 data = json.loads(request.body)
			 name = data['name']
			 company = data['company']
			 email = data['email']
			 contact = data['contact']
			 address = data['address']
			 taluk = data['taluk']
			 district = data['district']
			 state = data['state']
			 pincode = data['pincode']
			 zone = data['zone']
			 idc = data['id']
			 gstno = data['gstno']
			 form=Supplier.objects.filter(id=idc).update(name=name,company=company,contact=contact,email=email,address=address,taluk=taluk,district=district,state=state,pincode=pincode,zone=zone,gstno=gstno)
			 Suppliersbank = Supplierbankdetails.objects.filter(fid=idc)
			 Suppliersbank.delete()
			 count=len(data['bname'])
			 for x in range(count):
					bname=data['bname'][x]
					acno=data['acno'][x]
					ifsc=data['ifsc'][x]
					form1=Supplierbankdetails.objects.create(fid=idc,bankname=bname,accountno=acno,ifsccode=ifsc)
			 response = "success"
			 return JsonResponse({"msg":response}, status=201)
			 
		else:			
			 data['fail']="false"
			 return HttpResponse(data)			 
		 
#supplier details--------------------------------------------------------              

#sizing details--------------------------------------------------------
def sizing(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 return render(request, 'dashboard/sizing.html')

def getsizing(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		sizings = Sizing.objects.all()  
		data = serialize("json", sizings, fields=('id', 'name','company', 'contact', 'email', 'address', 'taluk', 'district', 'state', 'pincode', 'zone','gstno'))
		return HttpResponse(data)

def deletesizing(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		sizings = Sizing.objects.filter(id=id)
		sizings.delete()
		Sizingsbank = Sizingbankdetails.objects.filter(fid=id)
		Sizingsbank.delete()    
		response = "success"
		return JsonResponse({"msg":response}, status=201)

def editsizing(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		sizings = Sizing.objects.filter(id=id)  
		data = serialize("json", sizings, fields=('id', 'name','company', 'contact', 'email', 'address', 'taluk', 'district', 'state', 'pincode', 'zone','gstno'))
		return HttpResponse(data)

def editsizingbank(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Sizingbank = Sizingbankdetails.objects.filter(fid=id) 
		data = serialize("json", Sizingbank, fields=('id', 'bankname', 'accountno', 'ifsccode'))
		return HttpResponse(data)					

def addsizing(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		data={}
		if request.method == 'POST':
			 data = json.loads(request.body)
			 name = data['name']
			 company = data['company']
			 email = data['email']
			 contact = data['contact']
			 address = data['address']
			 taluk = data['taluk']
			 district = data['district']
			 state = data['state']
			 pincode = data['pincode']
			 zone = data['zone']
			 gstno = data['gstno']
			 form=Sizing.objects.create(name=name,company=company,contact=contact,email=email,address=address,taluk=taluk,district=district,state=state,pincode=pincode,zone=zone,gstno=gstno)
			 fid=Sizing.objects.filter(contact=contact).last().pk
			 count=len(data['bname'])
			 for x in range(count):
					bname=data['bname'][x]
					acno=data['acno'][x]
					ifsc=data['ifsc'][x]
					form1=Sizingbankdetails.objects.create(fid=fid,bankname=bname,accountno=acno,ifsccode=ifsc)
			 response = "success"
			 return JsonResponse({"msg":response}, status=201)
			 
		else:			
			 data['fail']="false"
			 return HttpResponse(data)

def updatesizing(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		data={}
		if request.method == 'POST':
			 data = json.loads(request.body)
			 name = data['name']
			 company = data['company']
			 email = data['email']
			 contact = data['contact']
			 address = data['address']
			 taluk = data['taluk']
			 district = data['district']
			 state = data['state']
			 pincode = data['pincode']
			 zone = data['zone']
			 idc = data['id']
			 gstno = data['gstno']
			 form=Sizing.objects.filter(id=idc).update(name=name,company=company,contact=contact,email=email,address=address,taluk=taluk,district=district,state=state,pincode=pincode,zone=zone,gstno=gstno)
			 Sizingsbank = Sizingbankdetails.objects.filter(fid=idc)
			 Sizingsbank.delete()
			 count=len(data['bname'])
			 for x in range(count):
					bname=data['bname'][x]
					acno=data['acno'][x]
					ifsc=data['ifsc'][x]
					form1=Sizingbankdetails.objects.create(fid=idc,bankname=bname,accountno=acno,ifsccode=ifsc)
			 response = "success"
			 return JsonResponse({"msg":response}, status=201)
			 
		else:			
			 data['fail']="false"
			 return HttpResponse(data)			 
		 
#sizing details--------------------------------------------------------  

#contractor details--------------------------------------------------------
def contractor(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 return render(request, 'dashboard/contractor.html')

def getcontractor(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		contractors = Contractor.objects.all()  
		data = serialize("json", contractors, fields=('id', 'name', 'contact', 'email', 'address', 'taluk', 'district', 'state', 'pincode', 'zone','gstno','profilephoto'))
		return HttpResponse(data)

def deletecontractor(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		contractors = Contractor.objects.filter(id=id)
		contractors.delete()
		Contractorbank = Contractorbankdetails.objects.filter(fid=id)
		Contractorbank.delete()      
		response = "success"
		return JsonResponse({"msg":response}, status=201)

def editcontractor(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		contractors = Contractor.objects.filter(id=id)  
		data = serialize("json", contractors, fields=('id', 'name', 'contact', 'email', 'address', 'taluk', 'district', 'state', 'pincode', 'zone','gstno','profilephoto','aadharno'))
		return HttpResponse(data)	

def editcontractorbank(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Contractorbank = Contractorbankdetails.objects.filter(fid=id) 
		data = serialize("json", Contractorbank, fields=('id', 'bankname', 'accountno', 'ifsccode','passbook'))
		return HttpResponse(data)								

def addcontractor(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		data1={}
		if request.method == 'POST':
			 data = json.loads(request.POST['data'])
			 name = data['name']
			 email = data['email']
			 contact = data['contact']
			 address = data['address']
			 taluk = data['taluk']
			 district = data['district']
			 state = data['state']
			 pincode = data['pincode']
			 zone = data['zone']
			 gstno = data['gstno']
			 aadharno = data['aadharno']
			 try:
				 profilephoto = request.FILES['file']
			 except:
				 profilephoto =""
			 form=Contractor.objects.create(name=name,contact=contact,email=email,address=address,taluk=taluk,district=district,state=state,pincode=pincode,zone=zone,gstno=gstno,aadharno=aadharno,profilephoto=profilephoto)
			 fid=Contractor.objects.filter(contact=contact).last().pk
			 count=len(data['bname'])
			 for x in range(count):
					bname=data['bname'][x]
					acno=data['acno'][x]
					ifsc=data['ifsc'][x]
					try:
						passbook = request.FILES['passbook'+str(x+1)]
					except:
						passbook =""  
					form1=Contractorbankdetails.objects.create(fid=fid,bankname=bname,accountno=acno,ifsccode=ifsc,passbook=passbook)
			 response = "success"
			 return JsonResponse({"msg":response}, status=201)
			 
		else:			
			 data1['fail']="false"
			 return HttpResponse(data1)

def updatecontractor(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		data={}
		if request.method == 'POST':
			 data = json.loads(request.POST['data'])
			 name = data['name']
			 email = data['email']
			 contact = data['contact']
			 address = data['address']
			 taluk = data['taluk']
			 district = data['district']
			 state = data['state']
			 pincode = data['pincode']
			 zone = data['zone']
			 idc = data['id']
			 gstno = data['gstno']
			 aadharno = data['aadharno']
			 try:
				 profilephoto = request.FILES['file']
				 form=Contractor.objects.filter(id=idc)
				 for obj in form:
						obj.name = name
						obj.profilephoto=profilephoto
						obj.contact=contact
						obj.email=email
						obj.address=address
						obj.taluk=taluk
						obj.district=district
						obj.state=state
						obj.pincode=pincode
						obj.zone=zone
						obj.aadharno=aadharno
						obj.gstno=gstno
						obj.save()
			 except:
				 form=Contractor.objects.filter(id=idc).update(name=name,contact=contact,email=email,address=address,taluk=taluk,district=district,state=state,pincode=pincode,zone=zone,aadharno=aadharno,gstno=gstno)	
			 Contractorbank = Contractorbankdetails.objects.filter(fid=idc)
			 Contractorbank.delete()
			 count=len(data['bname'])
			 for x in range(count):
					bname=data['bname'][x]
					acno=data['acno'][x]
					ifsc=data['ifsc'][x]
					try:
						passbook = request.FILES['passbook'+str(x+1)]
						form1=Contractorbankdetails.objects.create(fid=idc,bankname=bname,accountno=acno,ifsccode=ifsc,passbook=passbook)
					except:
						form1=Contractorbankdetails.objects.create(fid=idc,bankname=bname,accountno=acno,ifsccode=ifsc)	
			 response = "success"
			 return JsonResponse({"msg":response}, status=201)
			 
		else:			
			 data['fail']="false"
			 return HttpResponse(data)			 
		 
#contractor details--------------------------------------------------------  

def dashboard(request):
	return render(request, 'registration/login.html')    

def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = UserForm()

	 
	return render(request, 'registration/register.html',context={'form':form})

#factory details--------------------------------------------------------  

def factory(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		 return render(request, 'dashboard/factory_info.html')

def getfactory(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		cursor = connection.cursor()
		cursor.execute("SELECT a.`id`, `fname`, `faddress`,  `fkm`, `floomcount`,`name`,`contact` FROM login_factorymaster a inner join login_contractor b on a.cid=b.id")
		row = cursor.fetchall()
		#data= serialize("json",row)
		json_data = []
		for obj in row:
				 json_data.append({"cid" : obj[0], "fname" : obj[1],"faddress": obj[2],"fkm": obj[3],"floomcount": obj[4],"name": obj[5],"contact": obj[6]})

		return JsonResponse(json_data, safe=False)		

def addfactory(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:

		 if request.method == 'POST':
			 data = json.loads(request.body)
			 cid = data['cid']
			 fname=data['fname']
			 faddress=data['faddress']
			 fzone=data['fzone']
			 fkm=data['fkm']
			 flcount=data['flcount']
			 form=Factorymaster.objects.create(cid=cid,fname=fname,faddress=faddress,fzone=fzone,fkm=fkm,floomcount=flcount)
			 fid=Factorymaster.objects.filter(cid=cid).last().pk
			 count=len(data['lno'])
			 for x in range(count):
					lno=data['lno'][x]
					lname=data['lname'][x]
					lage=data['lapp'][x]
					lcategory=data['lcategory'][x]
					form1=Loomentry.objects.create(fid=fid,lno=lno,lname=lname,lwidth=lage,lcategory=lcategory)

			 response = "success"
			 return JsonResponse({"msg":response}, status=201)


def deletefactory(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Factory = Factorymaster.objects.filter(id=id)
		Factory.delete()
		Loom = Loomentry.objects.filter(fid=id)
		Loom.delete()      
		response = "success"
		return JsonResponse({"msg":response}, status=201)			 

def updatefactory(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:

		 if request.method == 'POST':
			 data = json.loads(request.body)
			 cid = data['cid']
			 idc = data['fid']
			 fname=data['fname']
			 faddress=data['faddress']
			 fzone=data['fzone']
			 fkm=data['fkm']
			 flcount=data['flcount']
			 form=Factorymaster.objects.filter(id=idc).update(cid=cid,fname=fname,faddress=faddress,fzone=fzone,fkm=fkm,floomcount=flcount)
			 Loomentrydel=Loomentry.objects.filter(fid=idc)
			 Loomentrydel.delete()
			 count=len(data['lno'])
			 for x in range(count):
					lno=data['lno'][x]
					lname=data['lname'][x]
					lage=data['lapp'][x]
					lcategory=data['lcategory'][x]
					form1=Loomentry.objects.create(fid=idc,lno=lno,lname=lname,lwidth=lage,lcategory=lcategory)

			 response = "success"
			 return JsonResponse({"msg":response}, status=201)		

def editfactory(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		cursor = connection.cursor()
		cursor.execute("SELECT a.`id`, `fname`, `faddress`,  `fkm`, `floomcount`,`name`,`contact`,`address`,`district`,b.`id`,`fzone` FROM login_factorymaster a inner join login_contractor b on a.cid=b.id where a.id=%s",[id])
		row = cursor.fetchall()
		#data= serialize("json",row)
		json_data = []
		for obj in row:
				 json_data.append({"cid" : obj[0], "fname" : obj[1],"faddress": obj[2],"fkm": obj[3],"floomcount": obj[4],"name": obj[5],"contact": obj[6],"address": obj[7],"district": obj[8],"contractorid": obj[9],"fzone": obj[10]})

		return JsonResponse(json_data, safe=False)

def editloom(request, id):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		Loomentrydata = Loomentry.objects.filter(fid=id) 
		data = serialize("json", Loomentrydata, fields=('lno', 'lname', 'lcategory', 'lage','ldoi'))
		return HttpResponse(data)												



		