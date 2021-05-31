from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
     
     #----------------------------------purchase--------------------------------------
      path('purchaseentry/',views.purchaseentry,name='purchaseentry'),
     path('getpurchaseview/<str:fromdate>/<str:todate>',views.getpurchaseview,name='getpurchaseview'),
     path('getmaterialpurchase/',views.getmaterialpurchase,name='getmaterialpurchase'),
     path('getpurchaseno/',views.getpurchaseno,name='getpurchaseno'),
     path('addmaterialpurchase/',views.addmaterialpurchase,name='addmaterialpurchase'),
     path('getmaterialpurchase/',views.getmaterialpurchase,name='getmaterialpurchase'),
     path('getmaterialpurchasemodel/',views.getmaterialpurchasemodel,name='getmaterialpurchasemodel'),
     path('deletematerialpurchase/<int:id>',views.deletematerialpurchase,name='deletematerialpurchase'),
      path('deletematerialpurchasemodel/',views.deletematerialpurchasemodel,name='deletematerialpurchasemodel'),
     path('editmaterialpurchase/<int:id>',views.editmaterialpurchase,name='editmaterialpurchase'),
     path('updatematerialpurchase/',views.updatematerialpurchase,name='updatematerialpurchase'),

     #--------------------------------sizing transfer-----------------------------------
     path('transfertosizing/',views.transfertosizing,name='transfertosizing'),
     path('gettransferview/<str:fromdate>/<str:todate>',views.gettransferview,name='gettransferview'),
     path('getmaterial/',views.getmaterial,name='getmaterial'),
     path('getreceiptno/',views.getreceiptno,name='getreceiptno'),
     path('addmaterialtransfer/',views.addmaterialtransfer,name='addmaterialtransfer'),
     path('getmaterialtransfer/',views.getmaterialtransfer,name='getmaterialtransfer'),
     path('getmaterialtransfermodel/',views.getmaterialtransfermodel,name='getmaterialtransfermodel'),
     path('deletematerialtransfer/<int:id>',views.deletematerialtransfer,name='deletematerialtransfer'),
      path('deletematerialtransfermodel/',views.deletematerialtransfermodel,name='deletematerialtransfermodel'),
     path('editmaterialtransfer/<int:id>',views.editmaterialtransfer,name='editmaterialtransfer'),
     path('updatematerialtransfer/',views.updatematerialtransfer,name='updatematerialtransfer'),
     ]