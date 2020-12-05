from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from .models import Product
from .models import Category
from .models import Customer
from .models import Orders
from .models import Contact


# Create your views here.
def index(request):
	if request.method == 'GET':
		cart = request.session.get('cart')
		if not cart:
			request.session.cart = {}
		product = None
		
		categories = Category.get_all_categories()
		categoryID = request.GET.get('category')
		if categoryID:

			product = Product.get_all_products_by_categoryid(categoryID)

		else:	

			product = Product.get_all_products()

		data = {}
		data['products'] = product 
		data['categories'] = categories 
		return render(request,'index.html',data)
	else:

		product = request.POST.get('product')
		remove = request.POST.get('remove')
		cart = request.session.get('cart')
		if cart:
			quantity = cart.get(product)
			if quantity:
				if remove:
					if quantity<=1:
						cart.pop(product)
					else:
						cart[product] = quantity - 1 
				else:
					cart[product] = quantity + 1
			else:
				cart[product] = 1
		else:
			cart = {}
			cart[product] = 1
		request.session['cart'] = cart
		print(request.session['cart'])
		return redirect('/')




def signup(request):
	if request.method == 'GET':
		return render(request, 'signup.html')
	else:

		first_name = request.POST.get('firstname')
		last_name = request.POST.get('lastname')
		phone = request.POST.get('phone')
		email = request.POST.get('email')
		password = request.POST.get('password')

		value = {
		'first_name':first_name,
		'last_name':last_name,
		'phone':phone,
		'email':email,
		}

		customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)

		error_msg = None

		#validation
		if not first_name:
			error_msg="Fist name required !"
		elif len(first_name)<4:
			error_msg = "Fist name must be 4 char long"
		elif not last_name:
			error_msg = "Last name reuired !"
		elif len(last_name)<4:
			error_msg = "Last name must be 4 character long"
		elif not phone:
			error_msg = "Phone number reuired !"
		elif len(phone)<10:
			error_msg = "phone number must be 10 Character long"
		elif not password:
			error_msg = "password required !"
		elif len(password)<6:
			error_msg = "This password is too short"
		elif len(email)<8:
			error_msg = "This is invalid email"
		elif customer.isExists():
			error_msg = "This Email Already registerd"

		#saving
		if not error_msg:
			customer.password = make_password(customer.password)
			customer.save()
			return redirect('/')
		else:
			data={
			'error':error_msg,
			'value':value
			}
			return render(request,'signup.html',data)

def login(request):
	if request.method == 'GET':
		return render(request,'login.html')
	else:
		email = request.POST.get('email')
		password = request.POST.get('password')
		customer = Customer.get_customer_by_email(email)
		error_msg = None
		if customer:
			flag = check_password(password,customer.password)
			if flag:
				request.session['customer'] = customer.id
				request.session['email'] = customer.email
				return redirect('/')
			else:
				error_msg = "Email or Password invalid"

		else:
			error_msg = "Email or Password invalid"
		return render(request,'login.html',{'error':error_msg})


def logout(request):
	request.session.clear()
	return redirect('/')


def cart(request):
	if request.method == 'GET':
		ids = request.session.get('cart')
		if ids:
			ids = list(request.session.get('cart').keys())
			products = Product.get_products_by_id(ids)
			return render(request,'cart.html',{'products':products})
		else:
			return render(request,'cart.html')

def checkout(request):
	address = request.POST.get('address')
	phone = request.POST.get('phone')
	customer = request.session.get('customer')
	if customer:
		cart = request.session.get('cart')
		products = Product.get_products_by_id(list(cart.keys()))
		
		for product in products:
			order = Orders(cutomer = Customer(id = customer),product = product,price = product.price,address = address,phone = phone,quantity = cart.get(str(product.id)))
			order.save()
		request.session['cart'] = {}
		return redirect('cart')
	else:
		return redirect('login')


def orderss(request):
	if request.method == 'GET':
		customer = request.session.get('customer')
		orders = Orders.get_orders_by_customer(customer)	
		return render(request,'orders.html',{'orders':orders})

def about(request):
	return render(request,'about.html')

def contact(request):
	if request.method == 'GET':
		return render(request,'contact.html')
	else:
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		message = request.POST.get('message')

		if email and name :
			contact = Contact(name=name,email=email,subject=subject,message=message)
			contact.save()
			msg = 'Your message sent successfully !'
			return render(request,'contact.html',{'msg':msg})
		else:
			error  = "Please Email and Name !"
			return render(request,'contact.html',{'error':error})


