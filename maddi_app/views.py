from django import template
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader

from .decorators import *
from .forms import *
from .models import *
import http.client

User = get_user_model()

# @login_required(login_url="/login/")
def index(request):
  return render(request, 'maddi_app/index.html')

def shop(request):
  item_list = Item.objects.all()
  paginator = Paginator(item_list, 12)

  page = request.GET.get('page', 1)
  try:
    items = paginator.page(page)
  except PageNotAnInteger:
    items = paginator.page(1)
  except EmptyPage:
    items = paginator.page(paginator.num_pages)

  return render(request, 'maddi_app/shop.html', {
    'items': items,
  })

@staff_required('index')
def create_item_view(request):
  form = ItemForm(request.POST or None, request.FILES or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('shop')

  return render(request, 'maddi_app/item/create.html', {
    'form': form,
  })

def retrieve_item_view(request, id):
  try:
    item = Item.objects.get(pk=id)
  except item.DoesNotExist:
    return redirect('shop')

  return render(request, 'maddi_app/item/retrieve.html', {
    'item': item,
  })

def user(request):
  user_list = User.objects.all()
  paginator = Paginator(user_list, 10)

  page = request.GET.get('page', 1)
  try:
    users = paginator.page(page)
  except PageNotAnInteger:
    users = paginator.page(1)
  except EmptyPage:
    users = paginator.page(paginator.num_pages)

  return render(request, 'maddi_app/user.html', {
    'users': users,
  })

@superuser_required('index')
def create_user_view(request):
  form = ProfileForm(request.POST or None, prefix='user')
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('user')

  context = {
    'form': form,
  }

  return render(request, 'accounts/create.html', context)

@superuser_required('index')
def update_user_view(request, id):
  try:
    user = User.objects.get(pk=id)
  except User.DoesNotExist:
    return redirect('user')
  
  form = ProfileForm(request.POST or None, prefix='user', instance=user)

  if request.method == 'POST':
    if form.is_valid():
      user = form.save(commit=False)
      password = make_password(form.cleaned_data['password'])
      if password:
        user.password = password

      user.save()

  context = {
    'form': form,
  }

  return render(request, 'accounts/create.html', context)

@staff_required('index')
def update_item_view(request, id):
  try:
    item = Item.objects.get(pk=id)
  except Item.DoesNotExist:
    return redirect('shop')
    
  form = ItemForm(request.POST or None, request.FILES or None, instance=item)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('shop')

  return render(request, 'maddi_app/item/create.html', {
    'form': form,
  })

@staff_required('index')
def delete_item_view(request, id):
  try:
    item = Item.objects.get(pk=id)
  except item.DoesNotExist:
    return redirect('shop')

  item.delete()
  return redirect('shop')

def payment(request):
  return render(request, 'maddi_app/payment.html')
  
def journal(request):
  return render(request, 'maddi_app/journal.html')

def about(request):
  return render(request, 'maddi_app/about.html')

def cart(request):
  cart_list = Cart.objects.filter(customer=request.user.customer)
  paginator = Paginator(cart_list, 10)

  page = request.GET.get('page', 1)
  try:
    carts = paginator.page(page)
  except PageNotAnInteger:
    carts = paginator.page(1)
  except EmptyPage:
    carts = paginator.page(paginator.num_pages)

  return render(request, 'maddi_app/cart.html', {
    'carts': carts,
  })

@login_required(login_url='login')
def add_to_cart(request):
  item = Item.objects.get(pk=request.POST.get('id'))
  print(item.price)
  cart = Cart(item=item, message=request.POST.get('message') or None, quantity=request.POST.get('quantity'), total_price=(item.price * int(request.POST.get('quantity'))), customer=request.user.customer)
  cart.save()

  return redirect('cart')

@login_required(login_url='login')
def profile_view(request):
  user_form = ProfileForm(request.POST or None, prefix='user', instance=request.user)
  if not request.user.is_superuser and not request.user.is_staff:
    customer_form = CustomerForm(request.POST or None, prefix='customer', instance=request.user.customer)

  if request.method == 'POST':
    if user_form.is_valid():
      user = user_form.save(commit=False)
      password = make_password(user_form.cleaned_data['password'])
      if password:
        user.password = password

      user.save()
      update_session_auth_hash(request, user)

      if not request.user.is_superuser and not request.user.is_staff:
        if customer_form.is_valid():
          customer = customer_form.save(commit=False)
          customer.user_id = user.id
          customer.save()

  if not request.user.is_superuser and not request.user.is_staff:
    context = {
      'user_form': user_form,
      'customer_form': customer_form
    }
  else:
    context = {
      'user_form': user_form,
    }

  return render(request, 'accounts/profile.html', context)

@anonymous_required('index')
def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('index')

    return render(request, 'accounts/login.html', {'form':form})

  form = AuthenticationForm()
  return render(request, 'accounts/login.html', {'form':form})

@anonymous_required('index')
def register_view(request):
  user_form = UserForm(request.POST or None, prefix='user')
  customer_form = CustomerForm(request.POST or None, prefix='customer')

  if request.method == 'POST':
    if user_form.is_valid():
      password = make_password(user_form.cleaned_data['password'])
      user = user_form.save(commit=False)
      user.password = password
      user.save()

      if customer_form.is_valid():
        customer = customer_form.save(commit=False)
        customer.user_id = user.id
        customer.save()

        return redirect('login')

  context = {
    'user_form': user_form,
    'customer_form': customer_form
  }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/')

def provinces(request):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': "833e8c949f70274cf9632f00c45919a8" }

  conn.request("GET", "/starter/province", headers=headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))

def cities(request, id=None):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': "833e8c949f70274cf9632f00c45919a8" }

  if id:
    conn.request("GET", f"/starter/city?province={id}", headers=headers)
  else:
    conn.request("GET", f"/starter/city", headers=headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))

def city(request, id):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': "833e8c949f70274cf9632f00c45919a8" }

  conn.request("GET", f"/starter/city?id={id}", headers=headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))

def cost(request, id):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  payload = f"origin=444&destination={id}&weight=1000&courier=jne"

  headers = {
    'key': "833e8c949f70274cf9632f00c45919a8",
    'content-type': "application/x-www-form-urlencoded"
  }

  conn.request("POST", "/starter/cost", payload, headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))
