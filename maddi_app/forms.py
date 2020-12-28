from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import *

class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  first_name = forms.CharField(required=True)
  last_name = forms.CharField(required=True)

  class Meta:
    model = get_user_model()
    fields = ['username', 'email', 'password', 'first_name', 'last_name']

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