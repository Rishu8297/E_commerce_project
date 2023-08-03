from django.http.response import HttpResponseRedirect
from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse,reverse_lazy
from app1.models import *
from django.views.generic import CreateView,UpdateView,ListView,DetailView,DeleteView
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from app1.forms import *
from django.http import HttpResponse,Http404

class MerchantMixin(LoginRequiredMixin,UserPassesTestMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    
    def test_func(self):
        return Merchant.objects.filter(user = self.request.user).exists()
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{self.login_url}?{self.redirect_field_name}={self.request.path}")
        
        return redirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        user_form = UserCreateForm(data = request.POST)
        customer_form = CustomerCreateForm(data = request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            u = user_form.save()
            customer = customer_form.save(commit = False)
            customer.user = u
            customer.save()
            return redirect(reverse_lazy('app1:products'))
        # print(user_form,customer_form)
        # process the data
    else:
        user_form = UserCreateForm()
        customer_form = CustomerCreateForm()
    return render(request,'register.html',{'user_form':user_form,
                                           'customer_form':customer_form})

def register_as_merchant(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    if request.method == 'POST':
        merchant_form = MerchantCreateForm(data = request.POST)
        if merchant_form.is_valid() :
            mer = merchant_form.save(commit = False)
            mer.user = request.user
            mer.started_at = datetime.now()
            mer.country = request.user.country
            mer.save()
            return redirect(reverse('index'))
    else:
        merchant_form = MerchantCreateForm()
        return render(request,'become_merchant.html',{'merchant_form':merchant_form})
    
def add_address(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    if request.method == 'POST':
        address_form = Add_Address_Form(data = request.POST)
        if address_form.is_valid():
            cus_address = address_form.save(commit= False)
            cus_address.user = request.user
            cus_address.save()
            return render(request,'index.html')
    else:
        address_form = Add_Address_Form()
        return render(request,'app1/add_address.html',{'address_form' : address_form})


def index(request):
    user = request.user
    ok = False
    if request.user.is_authenticated:
        if Merchant.objects.filter(user = request.user).exists():
            ok = True
    return render(request,'index.html',{'user':user,'ok':ok})

class ProductCreate(MerchantMixin,CreateView):
    form_class = ProductCreateForm
    template_name = 'app1/product_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.seller = self.request.user.merchant
        self.object.save()
        return super(ProductCreate,self).form_valid(form) #??

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					try:
						return render(request,'password/password_reset_email.html',{'c':c})
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
    

class ProductUpdate(MerchantMixin,UpdateView):
    form_class = ProductCreateForm
    template_name = 'app1/product_create.html'
    success_url = reverse_lazy('index')
    model = Product
    
class ProductList(LoginRequiredMixin,ListView):
    login_url = 'login'
    model = Product
    context_object_name = 'products'
    
class ProductDetail(LoginRequiredMixin,DetailView):
    model = Product
    content_object_name = 'product'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        # context['usertype'] = 'M' if Merchant.objects.filter(user = self.request.user).exists() else 'C'
        p_seller =  Product.objects.get(pk = self.get_object().pk)
        if p_seller.seller.user == self.request.user:
            context['usertype'] = 'M'
        else:
            context['usertype'] = 'C'
        return context

# def product_detail(request,pk):
#     if not request.user.is_authenticated:
#         return render(reverse('login'))
    

def buy_product(request,pk):
    print(pk)
    product = Product.objects.get(id =pk)
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            quantity = request.POST.get('quantity')
            # order_form = OrderCreateForm(request.POST)
            order = order_form.save(commit = False)
            order.buyer = request.user
            order.save()
            order_item = Order_item(quantity=quantity)
            order_item.order = order
            order_item.product = product
            order_item.price = product.price
            order_item.save()
            product.quantity -=  int(quantity)
            product.save()
            
            return redirect(reverse_lazy('app1:products'))
        else:
            return HttpResponse('Invalid Order')
    else :
        order_form = OrderCreateForm(user = request.user)
        n = range(1,product.quantity+1)
        return render(request,'app1/buy_product.html',{'order_form':order_form,'product':product,'n':n})
class ProductDelete(MerchantMixin,DeleteView):
    model = Product
    template_name = 'app1/product_delete_confirm.html'
    success_url = reverse_lazy('app1:products')


def get_orders(request):
    
    is_merchant = Merchant.objects.filter(user = request.user).exists()
    if not is_merchant:
        orders = Order.objects.filter(buyer = request.user)
    else:
        merchant = Merchant.objects.get(user = request.user)
        merchant_wala_order_itmes = Order_item.objects.filter(product__seller= merchant)
        orders = Order.objects.none()
        for  merchant_wala_order_item in  merchant_wala_order_itmes:
            orders |= Order.objects.filter(id =  merchant_wala_order_item.order.id)
    return render(request,'app1/orders.html',{'orders':orders})