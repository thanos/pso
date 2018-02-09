#
#   requestimpl.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: requestimpl.py,v 1.4 2002/04/21 23:16:51 thanos Exp $
#
__version__="$Revision: 1.4 $"

from resultcodes import  HTTP_MOVED_PERMANENTLY, HTTP_MOVED_TEMPORARILY 
from table import Table



class RequestImpl:
	_req=None
	def getOutStream(self): pass
	def getInStream(self): pass
	def getStatusCode(self, code): pass
	def getEnviron(self):pass 
	def getCookieKey(self): pass
	def send_http_header(self): pass

	def setup(self, handler, req):  pass
	def req(self):
		return self._req
	

        def setSession(self, handler, session): 
		session.setSession()
		
	def addHeaderOut(self, handler, key, value): 
		self.getHeadersOut().add(key, value)



	def redirect(self, handler, url, permanent):
		handler.setHeaderOut('location', url)
		if permanent:
			status = HTTP_MOVED_PERMANENTLY
		else:
			status = HTTP_MOVED_TEMPORARILY
		raise self.getServerReturn(), self.getStatusCode(status)

	
	def getStatusCode(self, code):
		return code

	def getServerReturn(self,code): 
		return SERVER_RETURN


	def getHeadersOut(self):
		return Table() 
	def syncHeadersOut(self, headers): pass

	def sendStatus(self, status):
		raise self.getServerReturn(), self.getStatusCode(status)

	def getInputs(self): pass
