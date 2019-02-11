# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse

	# import generic views
from django.views.generic import View, TemplateView
from django.views.generic.edit import UpdateView

	# import authenticate and login functionalities
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from django.forms.models import inlineformset_factory
from django import forms

	# import from models.py
from .models import ExtraInfo
from products.models import Product

	# import from forms.py
from .forms import loginForm, UserForm, extraInfoForm, updateBaseUserForm, updateExtraUserForm
from products.forms import addProductForm

from django.core.mail import send_mail
from django.conf import settings

	#
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
	#

	# Create your views here.

class initialView( TemplateView ):
	home_page = 'indexSeller.html'
	dashboard_page = 'sellerDashboard.html'

	form_login = loginForm

	def get( self, request, *args, **kwargs ):
		if request.user.is_authenticated:
			print( '\n\tUser is authenticated, redirect to Dashboard\n' )
				# redirect user to dashboard
			message = 'Access Granted'
			args = {
				'status':message
			}
			return render( request, self.dashboard_page, args )
		else:
				# Allow user to login in using the blank login form
			flogin = self.form_login(None)
			if request.GET.get('status') != '':
				message = request.GET.get('status')
			else:
				message = ''

			args = {
				'signinForm':flogin,
				'status':message
			}

			return render( request, self.home_page, args )

		# end GET

	def post( self, request, *args, **kwargs ):
		lform = self.form_login( request.POST )
		if lform.is_valid():
			username = lform.cleaned_data['username']
			password = lform.cleaned_data['password']

			tologin_user = authenticate( username=username, password=password )
			if tologin_user is not None:
				if tologin_user.is_active:
					login( request, tologin_user )
						# create session
						# NB:Check for session > if request.session.has_key('loggedin_user'):
					request.session['loggedin_user'] = username
					message = '[ %s ] is Authenticated' % username
					args = {
						'status':message,
						'sellername':username
					}
					#return render( request, self.dashboard_page, args )
					return redirect( '/vendor/dashboard/?status=%s' % message )
				else:
					message = 'Your account has not been activated yet. Check email to activate it.'
					args = {
						'signinForm':lform,
						'status':message
					}
					return render( request, self.home_page, args )
			else:
				print( tologin_user )
				message = 'Invalid Credentials or In-active account, Please Try Again.'
				args = {
					'signinForm':lform,
					'status':message
				}
				return render( request, self.home_page, args )
		else:
			message = 'Invalid Credentials'
			args = {
				'signinForm':lform,
				'status':message,
			}
			return render( request, self.home_page, args )
		# end POST

	# end initialView

# view[ register page ]
class registerView( View ):
	register_page = 'registration_form.html'
	dashboard_page = 'sellerDashboard.html'

	form_default = UserForm
	#form_extra = extraInfoForm #->using "inlineformset_factory" to produce the form for "ExtraInfo"

	def get( self, request, *args, **kwargs ):
		fdefault = self.form_default(None)
		AccountInlineFormSet = inlineformset_factory( User, ExtraInfo, fields=('confirmPassword','profileImage','shop','shopInfo','shopLocation','website'), widgets={ 'confirmPassword':forms.PasswordInput(), 'shopLocation':forms.TextInput(attrs={'placeholder':'Nairobi'}), 'website':forms.TextInput(attrs={'placeholder':'https://example.com'}) } )
		fextra = AccountInlineFormSet(None)

		args = {
			'signupPart1':fdefault,
			'signupPart2':fextra
		}

		return render( request, self.register_page, args )
		# end GET
	def post( self, request, *args, **kwargs ):
		fdefault = self.form_default( request.POST )
		AccountInlineFormSet = inlineformset_factory( User, ExtraInfo, fields=('confirmPassword','profileImage','shop','shopInfo','shopLocation','website'), widgets={ 'confirmPassword':forms.PasswordInput(), 'shopLocation':forms.TextInput(attrs={'placeholder':'Nairobi'}), 'website':forms.TextInput(attrs={'placeholder':'https://example.com'}) } )
		fextra = AccountInlineFormSet( request.POST, request.FILES )

		if fdefault.is_valid():
			newseller = fdefault.save( commit=False )
			fextra = AccountInlineFormSet( request.POST, request.FILES, instance=newseller )
			if fextra.is_valid():
				username = fdefault.cleaned_data['username']
				password = fdefault.cleaned_data['password']
				new_vendor_email = fdefault.cleaned_data['email']
				new_vendor_email = '%s' % new_vendor_email
				print( '\n\tusername -- %s : email -- * %s *.\n' % (username,new_vendor_email) )

				for field in fextra:
					#print( field )
					confirmpwd = field.cleaned_data['confirmPassword']
					print( '\nto-confirm[- %s -]' % confirmpwd )
					if password != confirmpwd:
						message = 'Password Mismatch'
						print( '\n%s\n' % message )
						args = {
							'signupPart1':fdefault,
							'signupPart2':fextra,
							'status':message
						}
						return render( request, self.register_page, args )
						# end: password-checking
					# end: for-loop
						
				newseller.set_password( password )
				#newseller.is_active = False
				newseller.save()
				fextra.save()
				
				mail_subject = 'Registration Status of [ %s ]' % username
				mail_message = 'Welcome %s !, you have been registered. Authentication process underway. You may sign in, after you have activated your account.' % username
				mail_from = settings.EMAIL_HOST_USER
				recipient_list = [ new_vendor_email ]
				#send_mail( mail_subject, mail_message, mail_from, recipient_list, fail_silently=False, )
				
				newseller = authenticate( username=username, password=password )
				if newseller is not None:
					print( 'newseller is not None.\n' )
					newseller.is_active = False
					newseller.save()
					# sending activation email
					# nb: set 'is_active' to False :: user.is_active = False
					send_account_activation_email(request, newseller)
					#if newseller.is_active:
					message = 'You[ %s ] are now registered, check email to activate account.' % username
					print( '\n\tstatus -- %s .\n' % message )
					args = {
						'status':message
					}
					return render( request, 'registration_complete.html', args )
				else:
					print( '\tnewseller NOT authenticated\n' )
					#
			else:
				message = 'fextra is NOT valid'
				print( '\n\tstatus -- %s .\n' % message )
				args = {
					'signupPart1':fdefault,
					'signupPart2':fextra,
					'status':message
				}
				return render( request, self.register_page, args )
		else:
			message = 'fdefault is NOT valid'
			print( '\n\tstatus -- %s .\n' % message )
			args = {
				'signupPart1':fdefault,
				'signupPart2':fextra,
				'status':message
			}
			return render( request, self.register_page, args )

		message = 'No Processing'
		print( '\n\tstatus -- %s .\n' % message )
		args = {
			'signupPart1':fdefault,
			'signupPart2':fextra,
			'status':message
		}

		#return render( request, self.register_page, args )
		#return redirect( '/vendor/register/?status=%s' % message )
		# end POST
	# end registerView

	# send-activation-email
def send_account_activation_email(request, user):
	text_content = 'Account Activation Email'
	subject = 'Email Activation'
	template_name = "activation.html"
	from_email = settings.EMAIL_HOST_USER #DEFAULT_FROM_EMAIL
	# mail_from = settings.EMAIL_HOST_USER
	recipients = [ user.email ]
	kwargs = {
		"uidb64": urlsafe_base64_encode( force_bytes(user.pk) ).decode(),
		"token": default_token_generator.make_token( user )
	}
	activation_url = reverse("activate_user_account", kwargs=kwargs)

	activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

	context = {
        	'user': user,
        	'activate_url': activate_url
	}
	html_content = render_to_string(template_name, context)
	email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
	email.attach_alternative(html_content, "text/html")
	email.send()

	# activate-user-account
def activate_user_account( request, uidb64=None, token=None ):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64)) # urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except User.DoesNotExist:
		user = None
		# end : try-except

	if user and default_token_generator.check_token(user, token):
		user.is_email_verified = True
		user.is_active = True
		message = 'Your account has been activated. You can now access your account.'
		user.save()
		#login(request, user)
        	#return redirect('hr:user_profile')
        	#return redirect( '/vendor/dashboard/?status=%s' % message )
		args = {
			'status':message
		}
		return redirect( '/vendor/?status=%s' % message )
	else:
		return HttpResponse("Activation link has expired")
		# end : if-else

def logoutFunction( request ):
	if request.user.is_authenticated and request.session.has_key('loggedin_user'):
		tologout_user = request.user
		logout( request )
		try:
			del request.session['loggedin_user']
		except:
			pass
		message = 'Previous session destroyed'
		form_login = loginForm
		flogin = form_login(None)
		args = {
			'signinForm':flogin,
			'status':message,
		}
		return redirect( 'all_products' )
		#return redirect( '/vendor/?status=%s' % message )
		#return render( request, 'indexSeller.html', args )
	else:
		message = 'Access to logout process DENIED.'
		print( '\n\tstatus -- %s .\n' % message )
	# end logoutFunction

class dashboardView( View ):
	dashboard_page = 'sellerDashboard.html'
	login_page = 'indexSeller.html'
	form_addproduct = addProductForm #ongezaProduct #addProductForm

	def get( self, request, *args, **kwargs ):
		if request.session.has_key('loggedin_user') and request.user.is_authenticated : # ensure user is authenticated and session is active
			if request.GET.get('status') != '':
				message = request.GET.get('status')
				#print( '\n\tFrom url-query: %s ..\n' % message )
			else:
				message = ''

			fadd = self.form_addproduct(None)
			vendorProducts = Product.objects.filter( vendor=request.user )
			args = {
				'status':message,
				'formAddProduct':fadd,
				'vendorProducts':vendorProducts,
			}
			return render( request, self.dashboard_page, args )
		else:
			# redirect back to login page
			message = 'Please signIN to gain access.'
			form_login = loginForm
			flogin = form_login(None)
			args = {
				'signinForm':flogin,
				'status':message,
			}
			return render( request, 'indexSeller.html', args )
		# end GET
	def post( self, request, *args, **kwargs ):
		fadd = self.form_addproduct( self.request.POST, self.request.FILES )
		if fadd.is_valid():
			prodFormGot = fadd.save( commit=False )

			gotname = fadd.cleaned_data['name']
			message = 'Successfully Added[- %s -].' % gotname
			prodFormGot.vendor = request.user
			print( '\n\tset-vendor[ %s ].' % prodFormGot.vendor )
			print( '\t.. name[ %s ]-status[ %s ].\n' % (gotname,message) )
			prodFormGot.save()
			return redirect( '/vendor/dashboard/?status=%s' % message )
		else:
			message = 'form_addproduct is NOT valid'
			print( '\n.. %s ..\n' % message )
			vendorProducts = Product.objects.filter( vendor=request.user )
			args = {
				'status':message,
				'formAddProduct':fadd,
				'vendorProducts':vendorProducts,
			}
			#return redirect( '/vendor/dashboard/?status=%s' % message )
			return render( request, self.dashboard_page, args )
		# end POST

	# end dashboardView


	# update profile information
class updateProfileView( View ):
	edit_page = 'user_update_form.html'
	baseForm = updateBaseUserForm
	#extraForm = updateExtraUserForm
	UpdateUser_inlineformset = inlineformset_factory( User, ExtraInfo, fields=('profileImage','shop','shopInfo','shopLocation','website'), widgets={  } )

	def get( self, request, *args, **kwargs ):
		user = request.user
		fbase = self.baseForm( instance=user )
		fextra = self.UpdateUser_inlineformset( instance=user )

		args = {
			'fbase':fbase,
			'fextra':fextra,
		}

		return render( request, self.edit_page, args )
		
		# end get

	def post( self, request, *args, **kwargs ):
		user = request.user
		fbase = self.baseForm( request.POST, instance=user )
		fextra = self.UpdateUser_inlineformset( request.POST, request.FILES )

		if fbase.is_valid():
			updatedseller = fbase.save( commit=False )
			fextra = self.UpdateUser_inlineformset( request.POST, request.FILES, instance=updatedseller )
			
			if fextra.is_valid():
				updatedseller.save()
				#gotshop = fextra.cleaned_data['shop']
				#print(gotshop)
				fextra.save()
				message = 'Update Successful'
				return redirect( '/vendor/dashboard/?status=%s' % message )
			else:
				message = 'Invalid Data[Extra], Try Again'
				args = {
					'fbase':fbase,
					'fextra':fextra,
					'status':message,
				}

				return render( request, self.edit_page, args )

		else:
			message = 'Invalid Data, Try Again'
			args = {
				'fbase':fbase,
				'fextra':fextra,
				'status':message,
			}

			return render( request, self.edit_page, args )

		# end post