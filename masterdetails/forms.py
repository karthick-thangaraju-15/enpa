from django import forms  
from masterdetails.models import Contractor,Supplier,Sizing
from django.forms import ModelForm, Textarea


class ContractorForm(forms.ModelForm):  
    class Meta:  
        model = Contractor
        abstract = True
        fields="__all__"
        widgets = {
        'address': Textarea(attrs={'rows':80, 'cols':20}),
        

    }
class SupplierForm(forms.ModelForm):  
    class Meta:  
        model = Supplier
        abstract = True
        fields="__all__"
        widgets = {
        'address': Textarea(attrs={'rows':80, 'cols':20}),
        

    }

class SizingForm(forms.ModelForm):  
    class Meta:  
        model = Sizing
        abstract = True
        fields="__all__"
        widgets = {
        'address': Textarea(attrs={'rows':80, 'cols':20}),
        

    }        
    