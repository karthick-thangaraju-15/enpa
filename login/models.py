from __future__ import unicode_literals  
from django.db import models
import re
import os
from django.core.validators import RegexValidator
from phone_field import PhoneField
from uuid import uuid4
from django.utils import timezone
# from django.contrib.auth.models import AbstractBaseUser 
# from django.contrib.auth.models import UserManager



class Supplier(models.Model):
    re_alpha = re.compile('[^\W\d_]+$', re.UNICODE)
    
    name = models.CharField(max_length=30,validators=[RegexValidator(re_alpha, 'Only alphabetic')],verbose_name='Contractor Name') 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") 
    contact    = models.CharField(validators=[phone_regex], max_length=17)
    company    = models.CharField(max_length=30)
    email      = models.EmailField(max_length=50)  
    address    = models.CharField(max_length=80)
    taluk      = models.CharField(max_length=30)
    district   = models.CharField(max_length=30)
    state      = models.CharField(max_length=30)
    pincode    = models.CharField(max_length=8)
    zone       = models.CharField(max_length=8)
    gstno      = models.CharField(max_length=15,blank=True)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

   
    def __str__(self):
         return self.name

class Sizing(models.Model):
    re_alpha = re.compile('[^\W\d_]+$', re.UNICODE)
    
    name = models.CharField(max_length=30,validators=[RegexValidator(re_alpha, 'Only alphabetic')],verbose_name='Contractor Name') 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") 
    contact    = models.CharField(validators=[phone_regex], max_length=17)
    company    = models.CharField(max_length=30)
    email      = models.EmailField(max_length=50)  
    address    = models.CharField(max_length=80)
    taluk      = models.CharField(max_length=30)
    district   = models.CharField(max_length=30)
    state      = models.CharField(max_length=30)
    pincode    = models.CharField(max_length=8)
    zone       = models.CharField(max_length=8)
    gstno      = models.CharField(max_length=15,blank=True)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

   
    def __str__(self):
         return self.name

def path_and_rename(instance, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename) 

def path_and_renamepassbook(instance, filename):
    upload_to = 'passbook'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)          

class Contractor(models.Model):
    re_alpha = re.compile('[^\W\d_]+$', re.UNICODE)
    
    name = models.CharField(max_length=30,validators=[RegexValidator(re_alpha, 'Only alphabetic')],verbose_name='Contractor Name') 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") 
    contact    = models.CharField(validators=[phone_regex], max_length=17)
    email      = models.EmailField(max_length=50)  
    address    = models.CharField(max_length=80)
    taluk      = models.CharField(max_length=30)
    district   = models.CharField(max_length=30)
    state      = models.CharField(max_length=30)
    pincode    = models.CharField(max_length=8)
    zone       = models.CharField(max_length=8)
    profilephoto = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)
    gstno      = models.CharField(max_length=15,blank=True)
    aadharno   = models.CharField(max_length=12,blank=True)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

   
    def __str__(self):
         return self.name 

class District(models.Model):
    District    = models.CharField(max_length=8)
    State       = models.CharField(max_length=8)

class Factorymaster(models.Model):
    cid         = models.IntegerField()
    fname       = models.CharField(max_length=30) 
    faddress    = models.CharField(max_length=80)
    fzone       = models.CharField(max_length=30)
    fkm         = models.FloatField()
    floomcount  = models.IntegerField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

class Loomentry(models.Model):
    fid         = models.IntegerField()
    lname       = models.CharField(max_length=20) 
    lno         = models.CharField(max_length=5)
    lcategory   = models.CharField(max_length=20)
    lwidth        = models.FloatField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

class Supplierbankdetails(models.Model):
    fid         = models.IntegerField()
    bankname    = models.CharField(max_length=30) 
    accountno   = models.CharField(max_length=18)
    ifsccode    = models.CharField(max_length=20)


class Contractorbankdetails(models.Model):
    fid         = models.IntegerField()
    bankname    = models.CharField(max_length=30) 
    accountno   = models.CharField(max_length=18)
    ifsccode    = models.CharField(max_length=20)
    passbook    = models.ImageField(upload_to=path_and_renamepassbook, max_length=255, null=True, blank=True)

class Sizingbankdetails(models.Model):
    fid         = models.IntegerField()
    bankname    = models.CharField(max_length=30) 
    accountno   = models.CharField(max_length=18)
    ifsccode    = models.CharField(max_length=20) 

class Rawmaterial(models.Model):
    materialname      = models.CharField(max_length=30,blank=True)
    created    = models.DateTimeField(auto_now_add=True)

class Rawmaterialchild(models.Model):
    fid         = models.IntegerField()
    materialchild      = models.CharField(max_length=30,blank=True)
    created    = models.DateTimeField(auto_now_add=True)             
                       
  