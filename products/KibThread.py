# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from threading import local

_thread_locals = local()

def get_current_user():
	return getattr(_thread_locals, 'user', None)

class ThreadLocals( object ):
	"""Middleware that gets various objects from the request object and saves them in thread local storage."""
	def process_request( self, request ):
		_thread_locals.user = getattr( request, 'user', None )