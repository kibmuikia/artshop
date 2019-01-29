# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from .models import ExtraInfo

# login form
class loginForm( forms.Form ):
	username = forms.CharField( max_length=150 )
	password = forms.CharField( widget=forms.PasswordInput() )

# Default user information
class UserForm( forms.ModelForm ):
	class Meta:
		model = User
		fields = [ 'first_name', 'last_name', 'email', 'username', 'password' ]
		widgets = { 'password':forms.PasswordInput() }

# extra user information
class extraInfoForm( forms.ModelForm ):
	#confirmPassword = forms.CharField( max_length=32, widget=forms.PasswordInput, 
		#label='Confirm Password', help_text='Ensure password is the same' )
	class Meta:
		model = ExtraInfo
		fields = [ 'confirmPassword','profileImage', 'shop', 'shopInfo', 'shopLocation','website' ]
		widgets = { 'confirmPassword':forms.PasswordInput(), 'shopLocation':forms.TextInput(attrs={'placeholder':'Nairobi'}) }

	#fields_order = [ 'confirmPassword', 'profileImage', 'shop', 'shopInfo', 'website' ]
	def __init__(self, *args, **kwargs):
		super( extraInfoForm, self ).__init__(*args, **kwargs)
		self.fields.keyOrder = [ 'confirmPassword', 'profileImage', 'shop', 'shopInfo', 'website' ]

class updateBaseUserForm( forms.ModelForm ):
	class Meta:
		model = User
		fields = [ 'first_name', 'last_name', 'email' ]
class updateExtraUserForm( forms.ModelForm ):
	class Meta:
		model = ExtraInfo
		fields = [ 'profileImage', 'shop', 'shopInfo', 'shopLocation', 'website' ]