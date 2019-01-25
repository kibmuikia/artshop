# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

	# Default django-user model
from django.contrib.auth.models import User

	# Signals
from django.db.models.signals import post_save
 
# Create your models here.

	# Holds additional vendor information
class ExtraInfo( models.Model ):
	user = models.OneToOneField( User, primary_key=True, 
		on_delete=models.CASCADE, related_name='user' )

	confirmPassword = models.CharField( max_length=32, verbose_name='Confirm Password', 
		blank=False, null=True )

	profileImage = models.ImageField( upload_to='vendors/profileimages/',
	                        blank=True, default='', max_length=300,
	                        verbose_name='Profile Avatar' )

	shop = models.CharField( max_length=144, default='', blank=False,
						verbose_name='Business Name' )

	shopInfo = models.TextField( max_length=300, verbose_name='Business Description', default='',
		blank=False, help_text='Provide a brief decription of your business' )

	shopLocation = models.CharField( max_length=200, verbose_name='Business Location', default='', 
		blank=False )

	website = models.URLField( max_length=1000, verbose_name='Website', blank=True, 
		help_text='Begin with  "http://" or "https://" .' )

	status = models.IntegerField( default=0, null=False ) # 0=NotPaid, 1=Paid

	paidAmount = models.IntegerField( default=0 ) #before payment, amount is 0

	class Meta:
		verbose_name="Profile"

	def __str__(self):
		#return str(self.user)
		return str(self.user) + " (" + self.shop + ")"

	def save( self, *args, **kwargs ):
		# fileName :: profileImage
		if self.profileImage.name and len(self.profileImage.name) > 0:
			orginal_filename = self.profileImage.name
			orginal_filename = orginal_filename.lower()
			orginal_filename = orginal_filename.split('.')
			extension = orginal_filename[1]
			user_id = self.user.id
			user_name = self.user.username
			user_name = user_name.upper()
			mpya_filename = '{0}-{1}.{2}'.format( user_id, user_name, extension )
			self.profileImage.name = mpya_filename
		else:
			pass

		#print( self.user.password )
		#print( self.confirmPassword )

			# Now call the 'save' method
		super().save( *args, **kwargs )
		# end :: save

	# end ExtraInfo

# :: ensures that ExtraInfo-object is created, when a User-model-object is created
def create_account( sender, **kwargs ):
	user = kwargs[ "instance" ]
	if kwargs["created"]:
		ExtraInfo.objects.get_or_create( user=user )
		user_account = ExtraInfo( user=user )
		user_account.save()

post_save.connect( create_account, sender=User )