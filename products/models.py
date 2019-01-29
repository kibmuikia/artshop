# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

	# Default django-user model
from django.contrib.auth.models import User

from django.utils.text import slugify

# Create your models here.

class Category(models.Model):

	CLOTHING = 'CLOTHING'
	JEWELLERY = 'JEWELLERY'
	SCULPTURES = 'SCULPTURES'
	PAINTINGS = 'PAINTINGS'
	DRAWINGS = 'DRAWINGS'
	INTERIOR_DECOR = 'INTERIOR_DECOR'
	CARVINGS = 'CARVINGS'
	POTTERY = 'POTTERY'
	CROCKERY = 'CROCKERY'
	CRAFT_SUPPLIES = 'CRAFT_SUPPLIES'
	GIFT_CARDS = 'GIFT_CARDS'
	BAGS = 'BAGS'

	CATEGORY_CHOICES = (

		(CLOTHING,'Clothing & Fabric'),
		(JEWELLERY,'Jewellery'),
		(SCULPTURES,'Sculptures'),
		(PAINTINGS,'Paintings'),
		(DRAWINGS,'Drawings'),
		(INTERIOR_DECOR,'Interior Decor'),
		(CARVINGS,'Carvings'),
		(POTTERY,'Pottery'),
		(CROCKERY,'Crockery'),
		(CRAFT_SUPPLIES,'Craft Supplies'),
		(GIFT_CARDS,'Gift Cards'),
		(BAGS,'Bags')

	) # end : CATEGORY_CHOICES

	category = models.CharField( verbose_name="Product Category", max_length=250, blank=True,
							unique=True, null=True, default='' )

	categoryImage = models.ImageField( upload_to='categories/',
	                        blank=True, default='', max_length=300,
	                        verbose_name='Category Image' )

	class Meta:
		verbose_name ="Category"
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category

	def save( self, *args, **kwargs ):
		# fileName :: categoryImage
		if self.categoryImage.name and len(self.categoryImage.name) > 0:
			orginal_filename = self.categoryImage.name
			orginal_filename = orginal_filename.lower()
			orginal_filename = orginal_filename.split('.')
			extension = orginal_filename[1]
			category_name = self.category
			category_name = category_name.upper()
			mpya_filename = '{0}.{1}'.format( category_name, extension )
			self.categoryImage.name = mpya_filename
		else:
			pass

		self.slug = slugify(self.category)
			# Now call the 'save' method
		super().save( *args, **kwargs )
		# end :: save

class SubCategory(models.Model):

	EMBROIDERY = 'EMBROIDERY'
	KNITTED = 'KNITTED'
	CROTCHET = 'CROTCHET'
	BEADED = 'BEADED'
	WOOLLEN = 'WOOLLEN'
	MOSAIC = 'MOSAIC'
	WOODEN = 'WOODEN'
	SCREEN_PRINTED = 'SCREEN_PRINTED'
	WOVEN = 'WOVEN'
	LEATHER = 'LEATHER'

	SUBCATEGORY_CHOICES = (

		(EMBROIDERY,'Embroidery'),
		(KNITTED,'Knitted'),
		(CROTCHET,'Crotchet'),
		(BEADED,'Beaded'),
		(WOOLLEN,'Woollen'),
		(MOSAIC,'Mosaic'),
		(WOODEN,'Wooden'),
		(SCREEN_PRINTED,'Screen Printed'),
		(WOVEN,'Woven'),
		(LEATHER,'Leather')

	) # END : SUBCATEGORY_CHOICES

	sub_category = models.CharField( verbose_name="Product SubCategory", max_length=250, 
								blank=True, null=True, default='') # choices=SUBCATEGORY_CHOICES,

	#category = models.ForeignKey( Category, null=True, blank=True, on_delete=models.CASCADE )

	class Meta:
		verbose_name = "Sub-Category"
		verbose_name_plural = "Sub-Categories"
		pass

	def __str__(self):
		return self.sub_category # + " (" + self.category.category + ")"

	# function to define directory of product pictures

def product_picture_directory( instance, filename ):
	# 'products/user/%Y/%m-%d/'
	# 'products/%Y/%m'
	path = 'products/vendor_{0}/{1}'.format( instance.vendor.username, filename )
	return path

class Product( models.Model ):

	vendor = models.ForeignKey( User, on_delete=models.CASCADE )

	name = models.CharField( max_length=300, unique=True, 
		verbose_name='Product Name', primary_key=True )

	description = models.TextField( default='', blank=False, null=False, 
		verbose_name='Product Description' )

	prod_category = models.ForeignKey( Category, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Product Category")

	sub_category = models.ForeignKey( SubCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Product SubCategory")


	image_one = models.ImageField( upload_to=product_picture_directory, blank=False, null=True, 
		verbose_name='First Image', help_text='Choose an image for your product')

	image_two = models.ImageField( upload_to=product_picture_directory, blank=False, null=True, 
		verbose_name='Second Image' )

	image_three = models.ImageField( upload_to=product_picture_directory, blank=True, null=True, 
		verbose_name='Third Image' )

	price = models.IntegerField( verbose_name='Product Price', blank=False, default=0 )

	deliveryInfo = models.TextField( default='', blank=True, 
		verbose_name='Delivery Information' )

	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name + " (" + str(self.vendor) + ")"

	class Meta:
		ordering = ('name',)

	def save( self, *args, **kwargs ):
		#if self.profileImage.name and len(self.profileImage.name) > 0:
		if self.image_one.name and len(self.image_one.name) > 0:
			vendor = self.vendor.username
			productName = self.name

			one_original = self.image_one.name
			one_original = one_original.split('.')
			one_ext = one_original[1]
			one_new = '{0}-{1}.{2}'.format( vendor, productName, one_ext )
			self.image_one.name = one_new
		if self.image_two.name and len(self.image_two.name) > 0:
			vendor = self.vendor.username
			productName = self.name

			two_original = self.image_two.name
			two_original = two_original.split('.')
			two_ext = two_original[1]
			two_new = '{0}-{1}.{2}'.format( vendor, productName, two_ext )
			self.image_two.name = two_new
		if self.image_three.name and len(self.image_three.name) > 0:
			vendor = self.vendor.username
			productName = self.name

			three_original = self.image_three.name
			three_original = three_original.split('.')
			three_ext = three_original[1]
			three_new = '{0}-{1}.{2}'.format( vendor, productName, three_ext )
			self.image_three.name = three_new
		
		#toUse = exposed_request
		#print( type(toUse) )

		self.slug = slugify(self.name)
			# calling the save-method
		super(Product,self).save( *args, **kwargs )
		#super(FooBar, self).save(*args, **kwargs)

		# end : save()