from django.urls import path
from app1.views import *
app_name = 'app1'

urlpatterns = [
    path('product_create/',ProductCreate.as_view(),name='product_create'),
    path('product_update/<pk>/',ProductUpdate.as_view(),name='product_update'),
    path('product_detail/<pk>/',ProductDetail.as_view(),name='product_detail'),
    path('product_delete/<pk>/',ProductDelete.as_view(),name='product_delete'),
    path('buy_product/<pk>/',buy_product,name='buy_product'),
    path('products/',ProductList.as_view(),name='products'),
    path('orders/',get_orders,name='get_orders'),
    path('become_merchant/',register_as_merchant,name='register_as_merchant'),
    path('add_address/', add_address, name = 'add_address')
]