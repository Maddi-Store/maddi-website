from django.contrib.auth import get_user_model
from django.db import models
from smartfields import fields

class Customer(models.Model):
  user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
  phone_number = models.CharField(max_length=12)
  address = models.CharField(max_length=250)
  city = models.PositiveIntegerField()
  postal_code = models.IntegerField()
  
  def __str__(self) :
    return self.user.get_full_name()

class News(models.Model):
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  title = models.CharField(max_length=40)
  body = models.TextField()
  image = fields.ImageField(upload_to='news')
  date = models.DateTimeField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) :
    return self.title

class Category(models.Model):
  name = models.CharField(max_length=40)

  def __str__(self) :
    return self.name

class Item(models.Model):
  name = models.CharField(max_length=40)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  stock = models.IntegerField()
  price = models.IntegerField()
  description = models.TextField()
  image = fields.ImageField(upload_to='item')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) :
    return self.name

class Courrier(models.Model):
  name = models.CharField(max_length=40)

  def __str__(self) :
    return self.name

class Review(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  description = models.TextField()
  rating = models.FloatField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  items = models.ManyToManyField('Item', through='Cart', through_fields=('purchase', 'item'))
  cancellation = models.SmallIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  purchase = models.ForeignKey(Purchase, null=True, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  message = models.TextField(null=True)
  total_price = models.BigIntegerField()

class Shipping(models.Model):
  purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
  receiver_name = models.CharField(max_length=40)
  receiver_phone_number = models.CharField(max_length=12)
  receiver_address = models.CharField(max_length=250)
  receiver_city = models.PositiveIntegerField()
  receiver_city_name = models.CharField(max_length=50)
  receiver_postal_code = models.IntegerField()
  status = models.CharField(max_length=20)
  courrier = models.ForeignKey(Courrier, on_delete=models.CASCADE)
  shipping_price = models.BigIntegerField()
  date_shipped = models.DateTimeField(null=True)
  date_arrived = models.DateTimeField(null=True)

class Payment(models.Model):
  purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
  payment_amount = models.BigIntegerField()
  date_paid = models.DateTimeField(null=True)
  method = models.CharField(max_length=30)
  status = models.CharField(max_length=30)
  updated_at = models.DateTimeField(auto_now=True)
  image = fields.ImageField(null=True, upload_to='payment')
