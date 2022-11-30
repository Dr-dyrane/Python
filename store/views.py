from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 

from django.contrib.auth.models import User
from django.contrib import auth
from .filters import ProductFilter
from .serializers import UserSerializer
from .utils import cookieCart, cartData, guestOrder
from django.core.exceptions import MultipleObjectsReturned

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	category = Category.objects.all()

	products = Product.objects.all()    		    	
	context = {'products':products,'category':category, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)
	
	
	
def product_page(request, pk):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	product = Product.objects.get(id=pk)
	category = Category.objects.filter(name=product)
	
	context = {'items':items,'product':product, 'cartItems':cartItems , 'category':category,}
	return render(request, 'store/product.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def account(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	user = request.user.customer
	ship = ShippingAddress.objects.get(customer= user, order = order)
	

	context = {'items':items, 'user':user, 'order':order, 'cartItems':cartItems, 'ship':ship }
	return render(request, 'store/account.html', context)


def guest_account(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	user = request.user
	ship = ShippingAddress.objects.all()
	

	context = {'items':items, 'user':user, 'order':order, 'cartItems':cartItems, 'ship':ship }
	return render(request, 'store/guest_account.html', context)



def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def search(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    order = data['order']
    items = data['items']
    
    category = Category.objects.all()
    
    product = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product)
    context = {'cartItems':cartItems,'filter': product_filter ,'product':product,'category':category }
    return render(request, 'store/search.html', context)


def drug_class(request, pk):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	category = Category.objects.get(id=pk)
	product = Product.objects.filter(drug_class=category)
	    
	context = {'product':product,'category':category ,'cartItems':cartItems,}
	return render(request, 'store/drug_class.html', context)




def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	
	else:
	    customer, order = guestOrder(request, data)
	    
	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()   
	
	if order.shipping == True:
		ShippingAddress.objects.create(
		        customer=customer,
		        order=order,
		        address=data['shipping']['address'],
		        city=data['shipping']['city'],
		        state=data['shipping']['state'],
		        zipcode=data['shipping']['zipcode'],
		    )
		        
	return JsonResponse('Payment submitted..', safe=False)
	
	
def register(request):
    if request.method == "POST":
        try:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    User.objects.get(username = request.POST['username'])
                    return render (request,'store/register.html', {'error':'Username is already taken!'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    auth.login(request,user)
                    return redirect('store')
            else:
                error = {'error':'Password does not match!'}
                return render (request,'store/register.html',error )
        except ValueError:
            error = {'error':'Please input a valid username!'}
            return render (request,'store/register.html', error)
    else:
        return render(request,'store/register.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('store')
        else:
            error = {'error':'Username or password is incorrect!'}
            return render (request,'store/login.html', error)
    else:
        return render(request,'store/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('store')