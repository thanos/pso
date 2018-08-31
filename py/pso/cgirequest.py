
#
#   cgirequest.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: cgirequest.py,v 1.6 2002/05/22 02:21:31 thanos Exp $
#
__version__="$Revision: 1.6 $"

import sys
from request import  SERVER_RETURN
from requestimpl import RequestImpl
from copy import copy

	
class CgiRequest(RequestImpl):
	""" Concrete Implementation class for a CGI Request """

	COOKIE_KEY='HTTP_COOKIE'
	def __init__(self, req=None):
		#RequestImpl.__init__(self, req)
		self.ostream= sys.stdout

	def req(self):
		return self

	def getOutStream(self):
		return self.ostream

	def getCookieKey(self):
		return self.COOKIE_KEY

	def getEnviron(self, handler):
		import os
		env = copy(os.environ)
		return env
		
	def send_http_header(self, handler):
		handler.write(str(handler.getHeadersOut()))
		handler.write('\n')

	def getInputs(self, handler):
		from cgi import FieldStorage
		return FieldStorage()

	def getServerReturn(self):
		return SERVER_RETURN

