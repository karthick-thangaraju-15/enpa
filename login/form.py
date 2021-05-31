from django.contrib.auth.forms import UserCreationForm
from rest_framework import serializers
from django.contrib.auth.models import User
from django import forms 
from .models import Supplier,Contractor,Sizing,District


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email    = forms.EmailField(max_length=50)
    
    
    class Meta:  
        model = User
        abstract = True
        fields=('username','email')
        widgets = {
        'password': forms.PasswordInput(),
        'cpassword': forms.PasswordInput(),

    }

class SupplierForm(forms.ModelForm):
    
    class Meta:  
        model = Supplier
        abstract = True
        fields="__all__"

class SizingForm(forms.ModelForm):
    
    class Meta:  
        model = Sizing
        abstract = True
        fields="__all__"

class ContractorForm(forms.ModelForm):
    
    class Meta:  
        model = Contractor
        abstract = True
        fields="__all__"     

class DistrictForm(forms.ModelForm):
    
    class Meta:  
        model = District
        abstract = True
        fields="__all__"   

                 
      