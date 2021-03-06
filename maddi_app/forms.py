from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import ModelForm

import datetime

from .models import *

class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  first_name = forms.CharField(required=True)
  last_name = forms.CharField(required=True)

  class Meta:
    model = get_user_model()
    fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser']

class ProfileForm(UserForm):
  password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave this field blank to keep the old password.")

class CustomerForm(ModelForm):
  class Meta:
    model = Customer
    exclude = ['user']

class ItemForm(ModelForm):
  class Meta:
    model = Item
    fields = '__all__'

class NewsForm(ModelForm):
  class Meta:
    model = News
    fields = ['title', 'body', 'image', 'date']

  date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(attrs={'type': 'date'}))

class PaymentConfirmationForm(ModelForm):
  class Meta:
    model = Payment
    fields = ['image']

class ShipmentReceiptForm(ModelForm):
  class Meta:
    model = Shipping
    fields = ['delivery_receipt_number']