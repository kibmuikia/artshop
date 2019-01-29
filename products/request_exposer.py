# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from products import models

def RequestExposerMiddleware(get_response):
	def middleware(request):
		models.exposed_request = request
		response = get_response(request)
		return response

	return middleware