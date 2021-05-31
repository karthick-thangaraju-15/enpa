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

# Create your models here.
class Materialtransfer(models.Model):
    transferno     = models.IntegerField()
    transferdate   = models.DateField()
    sizing        = models.IntegerField()
    material      = models.IntegerField()
    count         = models.FloatField()
    gross_weight  = models.FloatField()
    net_weight    = models.FloatField()
    no_of_bags    = models.FloatField()
    gross_weight  = models.FloatField()
    number_of_cones  = models.IntegerField(blank=True)
    color_shadeandnumber = models.CharField(max_length=15,blank=True)
    user = models.IntegerField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

class Materialpurchase(models.Model):
    purchaseno     = models.IntegerField()
    purchasedate   = models.DateField()
    supplier      = models.IntegerField()
    material      = models.IntegerField()
    count         = models.FloatField()
    gross_weight  = models.FloatField()
    net_weight    = models.FloatField()
    no_of_bags    = models.FloatField()
    gross_weight  = models.FloatField()
    number_of_cones  = models.IntegerField(blank=True)
    color_shadeandnumber = models.CharField(max_length=15,blank=True)
    user = models.IntegerField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
