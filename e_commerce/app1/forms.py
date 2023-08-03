from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app1.models import *
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')
        
class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['mobile','gender','country']
        
class MerchantCreateForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['license_no','GST_no','address']

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','brand','colour','price','quantity','description','cover_image']

class Add_Address_Form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address','adr_type']
        
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address','payment_method']
    
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        self.fields['address'].queryset = Address.objects.filter(user = user)
        