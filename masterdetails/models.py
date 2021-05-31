from __future__ import unicode_literals  
from django.db import models
import re
from django.core.validators import RegexValidator
from phone_field import PhoneField
# from django.contrib.auth.models import AbstractBaseUser 
# from django.contrib.auth.models import UserManager



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
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

   
    def __str__(self):
         return self.name
