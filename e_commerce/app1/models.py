from django.db import models
from django.contrib.auth.models import User
# Create your models here.

GENDER_CHOICES = [
    ('M','Male'),
    ('F','Female'),
]
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=14)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    country = models.CharField(max_length=20)

class Merchant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    country = models.CharField(max_length=20)
    license_no = models.CharField(max_length=20)
    GST_no = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    colour = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    seller = models.ForeignKey(Merchant,on_delete= models.CASCADE)
    cover_image = models.ImageField(upload_to='covers/',null=True,blank=True)

    def __str__(self):
        return self.name
class Product_image(models.Model):
    product = models.ForeignKey(Product,on_delete= models.CASCADE)
    image = models.ImageField(upload_to='products/')    
    
ADR_CHOICES = [('H','HOME'),('O','OFFICE')]
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    adr_type = models.CharField(max_length=20,choices=ADR_CHOICES)

    def __str__(self):
        return self.address
        
PAYMENT_CHOICES = [
    ('COD','Cash On Delivery'),
    ('CARD','Credit/ Debit Card'),
    ('UPI','UPI')
]
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete= models.CASCADE)
    total = models.PositiveIntegerField(blank=True,null = True)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_CHOICES)
   
STATUS_CHOICES = [
    ('Placed','placed'),
    ('Dispatched', 'Dispatched'),
    ('Delievered' , 'Delievered'),
   ( 'Cancelled' , 'Cancelled')
   ]

class Order_item(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50,choices= STATUS_CHOICES,default='Placed') 
    price = models.PositiveIntegerField()
    