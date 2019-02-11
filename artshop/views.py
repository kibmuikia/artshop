# -*- coding: utf-8 -*-
from __future__ import unicode_literals

	# import generic views
from django.views.generic import View, TemplateView

from django.shortcuts import render, redirect

	# importing [ django-autocomplete-light v3 ]
from dal import autocomplete

from django.urls import reverse

	# import from products.models.py
from products.models import Category, Product

from django import forms

#from simple_autocomplete.widgets import AutoCompleteWidget

class searchProductsForm( forms.Form ):
	searchCat = forms.ModelChoiceField( queryset=Category.objects.all(), initial=3, 
		widget=autocomplete.ModelSelect2( url='products_autocomplete' ) )
	
	# end : searchProductsForm

	# views
class indexView( TemplateView ):
	template_name = 'index.html'
	form_searchcat = searchProductsForm

	def get( self, request, *args, **kwargs ):
		allCategories = Category.objects.all()
		fsearch = self.form_searchcat(None)
		args = {
			'allCategories':allCategories,
			'searchcategoryform':fsearch
		}
		return render( request, self.template_name, args )
		# end : get

	def post( self, request, *args, **kwargs ):
		toSearch = request.POST.get('searchtext', '')
		toSearchArray = toSearch.split(':')
		use = toSearchArray[0]
		message = 'searching for [ %s ]' % use
		print( message )
		return redirect( '/products/detail/%s' % use )
		# end : post

# for autocompleting 'Categories'
class ProductsAutocomplete( autocomplete.Select2QuerySetView ):
	# will initial provide autocomplete for the 'Category'-model
	def get_queryset(self):
		#qs = Country.objects.all()
		zoteCategory = Category.objects.all()

		if self.q:
			# qs = qs.filter(name__istartswith=self.q)
			zoteCategory = zoteCategory.filter( category__istartswith=self.q )

		return zoteCategory

	# end: ProductsAutocomplete