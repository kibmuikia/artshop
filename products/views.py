# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.urls import reverse_lazy

	# import generic views
from django.views.generic import View, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

	# import authenticate and login functionalities
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django import forms

from .models import Product, Category, SubCategory
from seller.models import ExtraInfo

from .forms import addProductForm, priceRangeForm

from django.core.paginator import Paginator

import simplejson as json

from dal import autocomplete

# Create your views here.

	# update product information
class updateProductView( UpdateView ):
	model = Product
	fields = [ 'name', 'description', 'prod_category', 'sub_category', 'image_one', 'image_two', 'image_three', 'price', 'deliveryInfo' ]
	template_name = 'product_update_form.html'
	#template_name_suffix = '_update_form'
	context_object_name = 'product'
	pk_url_kwarg = 'product_pk'

	def form_valid(self, form):
		product = form.save(commit=False)
		product.vendor = self.request.user
		product.save()
		message = 'product edited successfuly'
		print( message )
		return redirect( '/vendor/dashboard/?status=%s' % message )

	# delete product

class ProductDelete( DeleteView ):
	model = Product
	template_name = 'product_confirm_delete.html'

	def get_success_url(self):
		return reverse('dashboardLink')

class allproducts( View ):
	all_page = 'product_all.html'
	products_zote = Product.objects.all()

	pricerangeform = priceRangeForm

	def get( self, request, *args, **kwargs ):
		paginator = Paginator( self.products_zote, 3 ) # Show 15 products per page
		page = request.GET.get('page')
		products = paginator.get_page( page )

		pricerangeform = self.pricerangeform(None)

		args = {
			'zote':products,
			'pricerangeform':pricerangeform
		}

		return render( request, self.all_page, args )

		# end : get

	def post( self, request, *args, **kwargs ):
		toSearch = request.POST.get('searchtext', '')
		toSearchArray = toSearch.split(':')
		use = toSearchArray[0]
		message = 'searching for [ %s ]' % use
		print( message )
		return redirect( '/products/detail/%s' % use )

		# end : post

	# end: allproducts

def productsAutoComplete( request ):

	if request.GET: #is_ajax():#request.POST:
		q = request.GET.get('searchtext', '').capitalize()
		print(q)
		search_qs = Product.objects.filter(name__icontains=q)
		results = []
		for r in search_qs:
			use = '%s: in Category[ %s ]' % (r.name,r.prod_category)
			results.append(use)
		data = json.dumps(results)
		print( data )
	else:
		data = 'fail'

	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

class productDetail( DetailView ):

	model = Product
	template_name = 'product_detail.html'

	def get_context_data(self, **kwargs):
		context = super(productDetail, self).get_context_data(**kwargs)
		context['theseller'] = ExtraInfo.objects.filter( user=context['object'].vendor )
		print( context['theseller'] )
		#for det in context['theseller']:
			#print(det.shop)
		return context
	
	#def get( self, request, *args, **kwargs ):
		#pass

	#def post( self, request, *args, **kwargs ):
		#pass

	# end: productDetail

# vendor view
class vendorDetail( DetailView ):
	model = ExtraInfo
	template_name = 'product_vendor.html'

	"""def get_slug_field(self):
		return 'user__username'"""

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(vendorDetail, self).get_context_data(**kwargs)
		# Add extra context from another model
		context['product_model'] = Product.objects.filter( vendor=context['object'].pk )
		return context
		# END - get_context_data

	# END - vendorDetail

class productCategoryListView( ListView ):
	model = Product
	template_name = 'product_category.html'

	def get_queryset(self):
		return Product.objects.filter( prod_category=self.kwargs['pk'] )

		# END - get_queryset

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(productCategoryListView, self).get_context_data(**kwargs)
		# Add extra context from another model
		context['category_name'] = Category.objects.get( pk=self.kwargs['pk'] )
		print( context )
		return context
		# END - get_context_data """

	

	# END - 