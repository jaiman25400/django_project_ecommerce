from ecom.utils import cartData
from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.views.generic import (TemplateView, ListView)
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from .form import *
from django.contrib import messages
from django.core.mail import EmailMessage
import json
from django.conf import settings
from .form import ProfileUpdateForm

# Create your views here.


class HomeView(ListView):
	model = Product
	context_object_name = 'product_list'
	template_name = 'ecom/index.html'

	def get_queryset(self):
		return Product.objects.filter().order_by('-num_stock')[:20]


def category(request):
	categories = Category.get_all_categories()
	print(categories)
	categoryID = request.GET.get('category')

	if categoryID:
		print('cate if')
		products = Product.get_product_by_id(categoryID)
	else:
		print('cate else')
		products = Product.objects.all()
	context = {
		'categories': categories, 'products': products,
	}
	return render(request, 'ecom/category.html', context)


def product_details(request, slug):
	product = Product.objects.get(slug=slug)
	quantity = product.num_stock
	print('Quantity', quantity)
	if request.method == 'POST':
		return redirect('product_details', slug=slug)

	context = {
		'product': product, 'quantity': quantity,
	}
	return render(request, 'ecom/single-product.html', context)

# class CategoryView(ListView):
 #   model = Category
 #   template_name = 'ecom/category.html'
 #   context_object_name = 'category_list'
 #  categories = Category.objects.annotate(Count('product'))
 #  categories_num = Category.objects.annotate(num_products=Count('product'))
 #  print(categories_num)
 #  print(categories.values_list('name', 'product__count'))

	# def get_queryset(self):
	#    categories = Category.objects.annotate(Count('product'))
	#    count = categories.values_list('name', 'product__count')
	#    return count

	# def get_context_data(self, **kwargs):
 #   data = super().get_context_data(**kwargs)
 #   categories = Category.objects.annotate(Count('product'))
 #  data['list'] = categories.values_list('product__count')
 #   data['categories'] = categories_num = Category.objects.annotate(
 #      num_products=Count('product'))
 #   return data


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	profile = request.user.profile
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(
		profile=profile, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(
		profile=profile, order=order, product=product)  # if order item already exist we want to change it

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def cart(request):
	if request.user.is_authenticated:
		data = cartData(request)

		#cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		context = {'items': items, 'order': order, }
		return render(request, 'ecom/cart.html', context)
	else:
		return redirect('login')

def checkout(request):
	if request.user.is_authenticated:
		data = cartData(request)

		#cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		context = {'items': items, 'order': order, }
		return render(request, 'ecom/checkout.html', context)
	else:
		return redirect('login')

def processOrder(request):

	template = render_to_string('ecom/email_template.html',{'name':request.user.profile.name,})
	data = json.loads(request.body)
	print("data", data)
	if request.user.is_authenticated:
		profile = request.user.profile
		order, created = Order.objects.get_or_create(
			profile=profile, complete=False)
		print("if in", profile)
	# Checkout.html Form and Total is mentioned
	total = float(data['form']['total'])
	if total != 0:
		if total == order.get_final_total:
			order.complete = True
			order.price = total
			print("total", total)
		order.save()
	else:
		return JsonResponse('Add An item to cart..', safe=False)
	print("here shop")
	ShippingAddress.objects.create(
		profile=profile,
		addressLine1=data['shipping']['add1'],
		addressLine2=data['shipping']['add2'],
		city=data['shipping']['city'],
		zipcode=data['shipping']['zipcode'],
		country=data['shipping']['country'],
	)

	email = EmailMessage(
		'Thanks for Purchasing',
		template,
		settings.EMAIL_HOST_USER,
		[request.user.profile.email],
	)

	email.fail_silently = False	
	email.send()

	return JsonResponse('Payment submitted..', safe=False)


def search(request):
	print('helloo')
	if 'search' in request.GET:
		query = request.GET['search']
		if query:
			print('in query')
			qs = Product.objects.all().search(query)
			print('query if')
			print(query)
		else:
			print('query else')
			qs = None
	else:
		print('outer else')
		qs = None
	context = {
		'qs': qs
	}
	return render(request, 'ecom/search.html', context)


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('homepage')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			print('method is post')
			username = request.POST['username']
			password1 = request.POST['password1']
			password2 = request.POST['password2']
			email = request.POST['email']
			form = CreateUserForm(request.POST)
			if form.is_valid():
				print('form is valid')
				if User.objects.filter(username=username).exists():
					messages.info(request, 'Username Taken')
					return redirect('register')
				elif User.objects.filter(email=email).exists():
					messages.info(request, 'Email Taken')
					return redirect('register')
				else:
					print('in else')
					user = form.save()
					name = request.POST.get('first_name')
					lastName = request.POST.get('last_name')
					email = request.POST.get('email')
					mobile_no = request.POST.get('phone')
					Profile.objects.create(
						user=user, email=email, name=name, lastName=lastName, mobile_no=mobile_no)
					print('User Created')
					return redirect('login')

			#	user = form.save()
			#	name = request.POST['username']
			#	email = request.POST['email']
			#	Customer.objects.create(
			#		user = user,email=email,name=name
			#	)
				print('above user')
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' +
								 user)  # flash msg would popup

				return redirect('login')

		context = {'form': form}
		return render(request, 'ecom/register.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('homepage')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('homepage')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'ecom/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def confirmPage(request):
	profile = request.user.profile
	data = cartData(request)
	items = OrderItem.get_orderitem_by_customer(profile)
	order = Order.get_order_by_customer(profile)
	print('order',order)
	#item = order.orderitem_set.all()
	# print(order.save())
	context = {'items': items,'order':order }
	return render(request, 'ecom/confirmation.html', context)

def profilePage(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
			if p_form.is_valid():
				print('in if')
				p_form.save()
				messages.success(request, f'Your Account is Updated')
				return redirect('homepage')
		else:
			profile = request.user.profile
			p_form = ProfileUpdateForm(instance=request.user.profile)
	else: return redirect('login')
	context = {'p_form':p_form,'profile':profile}
	return render(request, 'ecom/profile.html', context)