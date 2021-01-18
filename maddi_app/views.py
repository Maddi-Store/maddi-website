from django import template
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader

from maddi.settings import EMAIL_HOST_USER

from .decorators import *
from .forms import *
from .models import *

import datetime
import http.client
from dateutil.relativedelta import relativedelta

User = get_user_model()
raja_ongkir_key = '41ba619db1e9c1ed92ae7cb1b59d9578'

def index(request):
  news = News.objects.filter(date__gt=datetime.datetime.now()).order_by('-date')[:3]
  items = Item.objects.all().order_by('-id')[:3]

  context = {
    'news': news,
    'items': items
  }
  return render(request, 'maddi_app/index.html', context)

def shop(request):
  if request.GET.get('search'):
    item_list = Item.objects.filter(name__icontains=request.GET.get('search')).order_by('-id')
  else:
    item_list = Item.objects.all().order_by('-id')
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

@superuser_required('index')
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

@superuser_required('index')
def delete_user_view(request, id):
  try:
    user = User.objects.get(pk=id)
  except User.DoesNotExist:
    return redirect('user')

  user.delete()
  return redirect('user')

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

@staff_required('item')
def delete_item_view(request, id):
  try:
    item = Item.objects.get(pk=id)
  except Item.DoesNotExist:
    return redirect('shop')

  item.delete()
  return redirect('shop')

def news(request):
  news_list = News.objects.filter(date__gt=datetime.datetime.now()).order_by('-date')
  paginator = Paginator(news_list, 10)

  page = request.GET.get('page', 1)
  try:
    news = paginator.page(page)
  except PageNotAnInteger:
    news = paginator.page(1)
  except EmptyPage:
    news = paginator.page(paginator.num_pages)

  return render(request, 'maddi_app/news.html', {
    'news': news,
  })

@staff_required('news')
def create_news_view(request):
  form = NewsForm(request.POST or None, request.FILES or None)
  if request.method == 'POST':
    if form.is_valid():
      news = form.save(commit=False)
      news.user_id = request.user.id
      news.save()
      return redirect('news')

  context = {
    'form': form,
  }

  return render(request, 'maddi_app/news/create.html', {
    'form': form,
  })

@staff_required('news')
def update_news_view(request, id):
  try:
    news = News.objects.get(pk=id)
  except News.DoesNotExist:
    return redirect('news')
    
  form = NewsForm(request.POST or None, request.FILES or None, instance=news)
  if request.method == 'POST':
    if form.is_valid():
      news = form.save(commit=False)
      news.user_id = request.user.id
      news.save()
      return redirect('news')

  context = {
    'form': form,
  }

  return render(request, 'maddi_app/news/create.html', {
    'form': form,
  })

@staff_required('news')
def delete_news_view(request, id):
  try:
    news = News.objects.get(pk=id)
  except News.DoesNotExist:
    return redirect('news')

  news.delete()
  return redirect('news')

def about(request):
  return render(request, 'maddi_app/about.html')

@login_required(login_url='login')
def cart(request):
  carts = Cart.objects.filter(customer=request.user.customer, purchase__isnull=True)
  total_price = carts.aggregate(Sum('total_price'))

  return render(request, 'maddi_app/cart.html', {
    'carts': carts,
    'total_price': total_price
  })

@login_required(login_url='login')
def add_to_cart(request):
  item = Item.objects.get(pk=request.POST.get('id'))
  
  try:
    cart = Cart.objects.get(customer=request.user.customer, purchase__isnull=True, item=item)
    cart.quantity += int(request.POST.get('quantity'))
    cart.total_price += item.price * int(request.POST.get('quantity'))
  except Cart.DoesNotExist:
    cart = Cart(item=item, message=request.POST.get('message') or None, quantity=request.POST.get('quantity'), total_price=(item.price * int(request.POST.get('quantity'))), customer=request.user.customer)

  cart.save()

  return redirect('cart')

@login_required(login_url='login')
def update_cart_view(request):
  cart = Cart.objects.get(pk=request.POST.get('id'))
  cart.message = request.POST.get('message')
  cart.quantity = request.POST.get('quantity')
  cart.total_price = cart.item.price * int(cart.quantity)
  cart.save()

  return redirect('cart')

@login_required(login_url='login')
def delete_cart_view(request, id):
  cart = Cart.objects.get(pk=id)
  cart.delete()

  return redirect('cart')

@login_required(login_url='login')
def checkout(request):
  customer_form = CustomerForm(request.POST or None, instance=request.user.customer)
  if request.method == 'POST':
    purchase = Purchase(customer=request.user.customer, cancellation=0)
    purchase.save()

    post = request.POST
    shipping = Shipping(purchase=purchase, receiver_name=post.get('receiver_name'), receiver_phone_number=post.get('phone_number'),
      receiver_address=post.get('address'), receiver_city=post.get('city'), receiver_city_name=post.get('shipping_city'), receiver_postal_code=post.get('postal_code'), 
      status='belum', courrier=Courrier.objects.get(pk=int(post.get('courrier'))), shipping_price=post.get('shipping_price')
    )
    shipping.save()

    payment = Payment(purchase=purchase, payment_amount=int(post.get('payment_price')), status='belum', method=post.get('payment_method'))
    payment.save()
    
    carts = Cart.objects.filter(customer=request.user.customer, purchase__isnull=True)
    for cart_item in carts:
      item = Item.objects.get(pk=cart_item.item_id)
      item.stock = item.stock - cart_item.quantity
      item.save()

    carts.update(purchase=purchase)
    
    return redirect('retrieve_purchase', id=purchase.id)

  carts = Cart.objects.filter(customer=request.user.customer, purchase__isnull=True)
  total_price = carts.aggregate(Sum('total_price'))

  context = {
    'customer_form': customer_form,
    'total_price': total_price
  }
  return render(request, 'maddi_app/checkout.html', context)

@login_required(login_url='login')
def payment_method(request):
  return render(request, 'maddi_app/payment_method.html')

@login_required(login_url='login')
def purchase(request):
  if request.user.is_staff == False and request.user.is_superuser == False:
    purchases_list = Purchase.objects.filter(customer=request.user.customer).order_by('-id')
  else:
    purchases_list = Purchase.objects.all().order_by('-id')

  paginator = Paginator(purchases_list, 10)

  page = request.GET.get('page', 1)
  try:
    purchases = paginator.page(page)
  except PageNotAnInteger:
    purchases = paginator.page(1)
  except EmptyPage:
    purchases = paginator.page(paginator.num_pages)

  return render(request, 'maddi_app/purchase.html', {
    'purchases': purchases
  })

@login_required(login_url='login')
def retrieve_purchase_view(request, id):
  purchase = Purchase.objects.get(pk=id)
  carts = Cart.objects.filter(purchase=purchase)
  total_price = carts.aggregate(Sum('total_price'))

  context = {
    'purchase': purchase,
    'carts': carts,
    'total_price': total_price
  }

  if not request.user.is_staff and not request.user.is_superuser:
    form = PaymentConfirmationForm(request.POST or None, request.FILES or None, instance=purchase.payment)
    context['form'] = form
    if request.method == 'POST' and form.is_valid():
      form.save()
      purchase.payment.status = 'sudah'
      purchase.payment.save()

      subject = f'MADDI | Payment Proof Uploaded by {request.user}'
      message = f'You have a payment proof to be reviewed from {request.user}'
      recepient = 'segara2410@gmail.com'
      send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

  else:
    form = ShipmentReceiptForm(request.POST or None, instance=purchase.shipping)
    context['form'] = form
    if request.method == 'POST' and form.is_valid():
      form.save()
      purchase.shipping.status = 'sudah'
      purchase.shipping.save()

  return render(request, 'maddi_app/purchase/retrieve.html', context)

@staff_required('purchase')
def process_payment_proof_view(request, id):
  purchase = Purchase.objects.get(pk=id)
  purchase.payment.status = request.POST.get('status')
  purchase.payment.date_paid = datetime.datetime.now()
  purchase.payment.save()

  return redirect('retrieve_purchase', id)

@login_required(login_url='login')
def complete_purchase_view(request, id):
  purchase = Purchase.objects.get(pk=id)
  purchase.shipping.status = 'diterima'
  purchase.shipping.save()
  return redirect('retrieve_purchase', id)

@login_required(login_url='login')
def cancel_purchase_view(request, id):
  purchase = Purchase.objects.get(pk=id)
  carts = Cart.objects.filter(purchase=purchase)
  
  for cart_item in carts:
    item = Item.objects.get(pk=cart_item.item_id)
    item.stock = item.stock + cart_item.quantity
    item.save()

  carts.delete()
  purchase.delete()
  return redirect('purchase')

@superuser_required('index')
def report_weekly(request):
  return render(request, 'maddi_app/report_weekly.html')

@superuser_required('index')
def report_monthly(request):
  return render(request, 'maddi_app/report_monthly.html')

@superuser_required('index')
def report_yearly(request):
  return render(request, 'maddi_app/report_yearly.html')

@login_required(login_url='login')
def profile_view(request):
  user_form = ProfileForm(request.POST or None, prefix='user', instance=request.user)
  if not request.user.is_superuser and not request.user.is_staff:
    customer_form = CustomerForm(request.POST or None, prefix='customer', instance=request.user.customer)

  if request.method == 'POST':
    if user_form.is_valid():
      user = user_form.save(commit=False)
      if user_form.cleaned_data['password']:
        password = make_password(user_form.cleaned_data['password'])
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

@login_required(login_url='login')
def logout_view(request):
  logout(request)
  return redirect('/')

def provinces(request):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': raja_ongkir_key }

  conn.request("GET", "/starter/province", headers=headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))

def cities(request, id=None):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': raja_ongkir_key }

  if id:
    conn.request("GET", f"/starter/city?province={id}", headers=headers)
  else:
    conn.request("GET", f"/starter/city", headers=headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))

def city(request, id):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  headers = { 'key': raja_ongkir_key }

  conn.request("GET", f"/starter/city?id={id}", headers=headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))

def cost(request, id):
  conn = http.client.HTTPSConnection("api.rajaongkir.com")

  payload = f"origin=444&destination={id}&weight=1000&courier=jne"

  headers = {
    'key': raja_ongkir_key,
    'content-type': "application/x-www-form-urlencoded"
  }

  conn.request("POST", "/starter/cost", payload, headers)

  res = conn.getresponse()
  data = res.read()

  return HttpResponse(data.decode("utf-8"))


@superuser_required('index')
def chart_maddi_yearly(request):
  labels = []
  data = []
  queryset = Payment.objects.filter(date_paid__gte=datetime.datetime.now()-relativedelta(years=10)).annotate(year=TruncYear('date_paid')).values('year').annotate(pendapatan=Sum('payment_amount')).values('year', 'pendapatan').order_by('year')

  for entry in queryset:
    labels.append(entry['year'].strftime("%Y"))
    data.append(entry['pendapatan'])
  
  return JsonResponse(data={
    'labels': labels,
    'data': data,
  })

@superuser_required('index')
def chart_maddi_monthly(request):
  labels = []
  data = []
  queryset = Payment.objects.filter(date_paid__gte=datetime.datetime.now()-relativedelta(years=1)).annotate(month=TruncMonth('date_paid'), year=TruncYear('date_paid')).values('month', 'year').annotate(pendapatan=Sum('payment_amount')).values('month', 'year', 'pendapatan').order_by('year', 'month')

  for entry in queryset:
    labels.append(entry['month'].strftime("%b") + ' ' + entry['year'].strftime("%Y"))
    data.append(entry['pendapatan'])
  
  return JsonResponse(data={
    'labels': labels,
    'data': data,
  })

@superuser_required('index')
def chart_maddi_weekly(request):
  labels = []
  data = []
  queryset = Payment.objects.filter(date_paid__gte=datetime.datetime.now()-relativedelta(months=3)).annotate(date=TruncDate('date_paid'), month=TruncMonth('date_paid'), year=TruncYear('date_paid')).values('date', 'month', 'year').annotate(sum=Sum('payment_amount')).order_by('year', 'month', 'date')

  for entry in queryset:
    print(entry)
    try:
      index = labels.index('Week ' + str((entry['date'].day-1)//7+1) + ' of ' + entry['month'].strftime("%B"))
      data[index] += entry['sum']
    except ValueError:
      labels.append('Week ' + str((entry['date'].day-1)//7+1) + ' of ' + entry['month'].strftime("%B"))
      data.append(entry['sum'])
  
  return JsonResponse(data={
    'labels': labels,
    'data': data,
  })