# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
	
	# home/index page for app[ seller ]
	url( r'^$', views.initialView.as_view(), name="sellerIndex" ), # To Use As Login-Form

	url( r'^register/$', views.registerView.as_view(), name="sellerRegister" ), # Registration Form Page

	# logout function
	url( r'^logout/$', views.logoutFunction, name='logoutLink' ),

	# activate-account function
	#url( r'^activate/$', views.activate_user_account, name='activate_user_account' ),

	# view Dashboard
	url( r'^dashboard/$', views.dashboardView.as_view(), name='dashboardLink' ),

	# to edit profile
	url( r'^dashboard/edit/(?P<profile_pk>.+)/$', views.updateProfileView.as_view(), name="edit_profile" ),

	# activate-account-url
	url( r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/account/$',
        views.activate_user_account, name='activate_user_account' ),

]