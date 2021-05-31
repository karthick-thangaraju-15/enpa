from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
     path('',views.index,name='index'),
     path('register/',views.register,name='register'),
     path('getmaster/',views.getmaster,name='getmaster'),

     path('mastersupplier/',views.supplier,name='supplier'),
     path('mastercontractor/',views.contractor,name='contractor'),
     path('districtget/<slug:state>',views.districtget,name='districtget'),
     path('mastersizing/',views.sizing,name='sizing'),
     path('getsupplier/',views.getsupplier,name='getsupplier'),
     path('addsupplier/',views.addsupplier,name='addsupplier'),
     path('editsupplier/<int:id>',views.editsupplier,name='editsupplier'),
     path('editsupplierbank/<int:id>',views.editsupplierbank,name='editsupplierbank'),
     path('deletesupplier/<int:id>',views.deletesupplier,name='deletesupplier'),
     path('updatesupplier/',views.updatesupplier,name='updatesupplier'),
     path('getsizing/',views.getsizing,name='getsizing'),
     path('addsizing/',views.addsizing,name='addsizing'),
     path('editsizing/<int:id>',views.editsizing,name='editsizing'),
     path('editsizingbank/<int:id>',views.editsizingbank,name='editsizingbank'),
     path('updatesizing/',views.updatesizing,name='updatesizing'),
     path('deletesizing/<int:id>',views.deletesizing,name='deletesizing'),
     path('updatecontractor/',views.updatecontractor,name='updatecontractor'),
     path('getcontractor/',views.getcontractor,name='getcontractor'),
     path('addcontractor/',views.addcontractor,name='addcontractor'),
     path('editcontractor/<int:id>',views.editcontractor,name='editcontractor'),
     path('editcontractorbank/<int:id>',views.editcontractorbank,name='editcontractorbank'),
     path('deletecontractor/<int:id>',views.deletecontractor,name='deletecontractor'),
     path('updatecontractor/',views.updatecontractor,name='updatecontractor'),
     path('masterfactory/',views.factory,name='factory'),
     path('addfactory/',views.addfactory,name='addfactory'),
     path('getfactory/',views.getfactory,name='getfactory'),
     path('editfactory/<int:id>',views.editfactory,name='editfactory'),
     path('updatefactory/',views.updatefactory,name='updatefactory'),
     path('deletefactory/<int:id>',views.deletefactory,name='deletefactory'),
     path('editloom/<int:id>',views.editloom,name='editloom'),


  ]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)