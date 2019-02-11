# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

	# import models
from .models import ExtraInfo

class profileExtraInline(admin.TabularInline):
	model = ExtraInfo
	extra = 1
	can_delete = False

# Register your models here.
admin.site.register( ExtraInfo )