"""artshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = 'seller'

urlpatterns = [
	#path('admin/', admin.site.urls),
	url( r'^admin/', admin.site.urls ),

	# site index page
	url( r'^$', views.indexView.as_view(), name='mainIndexLink' ),

	# application[ seller ]
	url( r'^vendor/', include( 'seller.urls' ) ),
	#url(r'^reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),

	# application[ products ]
	url( r'^products/', include( 'products.urls' ) ),

	# for autocomplete dal
	url( r'^products_autocomplete/$', views.ProductsAutocomplete.as_view(), name='products_autocomplete' ),

	# for [ simple autocomplete ]
	#url( r'^simple-autocomplete/', include(('simple_autocomplete.urls', 'simple_autocomplete'), namespace='simple_autocomplete' ) ),

	# for reviews
	#url( r'^review/', include('review.urls') ),

	# star ratings .. , app_name='ratings'
	url(r'^ratings/', include('star_ratings.urls', namespace='ratings' ) ),

]

if settings.DEBUG is True:
	urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )