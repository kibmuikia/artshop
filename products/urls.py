# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
	
	# home/index page for app[ products ]
	#url( r'^$', views.indexView.as_view(), name="productsIndex" ), 
	# updateProductView ProductDelete

	# to edit product
	url( r'^edit/(?P<product_pk>.+)/$', views.updateProductView.as_view(), name="edit_product" ),

	# to delete product
	url( r'^delete/(?P<slug>.+)/$', views.ProductDelete.as_view(), name="delete_product" ),

	# to view all products
	url( r'^all/$', views.allproducts.as_view(), name='all_products' ),

	# search products autocomplete
	url( r'^ajax_calls/search/', views.productsAutoComplete, name='productsAutoCompleteLink' ),

	# product detail view
	url( r'^detail/(?P<slug>.+)/$', views.productDetail.as_view(), name='product_detail_link' ),

	# vendor detail view
	url( r'^vendorDetails/(?P<pk>.+)/$', views.vendorDetail.as_view(), name='vendor_detail_link' ),

	# category list view
	url( r'^category/(?P<pk>.+)/$', views.productCategoryListView.as_view(), name='category_list_link' ),

]