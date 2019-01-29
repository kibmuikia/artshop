# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User

from .models import Product, Category, SubCategory

"""from django_range_slider.fields import RangeSliderField"""
from .fields import RangeSliderField

# ADD product form
class addProductForm( forms.ModelForm ):

	class Meta:
		model = Product
		#exclude = ['vendor']
		fields = [ 'name', 'description', 'price', 'prod_category', 'sub_category', 'image_one', 'image_two', 'image_three', 'deliveryInfo' ]
		#widgets = { 'vendor':forms.HiddenInput() }

	# end addProductForm

class priceRangeForm(forms.Form):
	price_range_field = RangeSliderField(minimum=50,maximum=500000,name="pricerange",label="Price Range") # with name inside the input field (no label)