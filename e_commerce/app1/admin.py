from django.contrib import admin
from app1.models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Merchant)
admin.site.register(Product_image)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Product)