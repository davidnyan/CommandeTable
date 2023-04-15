from django.forms import ModelForm
from django import forms
from .models import Order,Sale
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class signinForm(ModelForm):
   
    class Meta:
        model=User
        fields=['username','password']
       
class CartForm(forms.Form):
    quantite = forms.IntegerField(initial='1')
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CartForm, self).__init__(*args, **kwargs)


        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('Servir','encourspreparation','Serveur','Nom','Tel')


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields="__all__"



