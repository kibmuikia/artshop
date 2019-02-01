# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

	# import models
from .models import Category, SubCategory, Product

# Register your models here.
admin.site.register( Category )
admin.site.register( SubCategory )
admin.site.register( Product )