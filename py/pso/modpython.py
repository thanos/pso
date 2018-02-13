#
#   modpython.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: modpython.py,v 1.9 2002/04/21 23:16:51 thanos Exp $
#
__version__="$Revision: 1.9 $"

from pso import service
from cgirequest import CgiRequest

from mod_python import apache, util

def fixup(req, sessionImpl=None): 
	service.fixup(req, ModPythonRequest, sessionImpl = sessionImpl )
	return apache.OK

def cleanup(req):
	service.cleanup(req)
	return apache.OK


class FormInput(util.FieldStorage):
	def getvalue(key, default=None):
		reval = default
		if self.has_key(key):
			value = self[key]
			if type(value) is type([]):
				retval =  map(lambda v:v.value, value)
			else:
				retval =  value.value
		return retval
	
	def getfirst(self, key, default =None):
		retval = default
		if self.has_key(key):
			value = self[key]
			if type(value) is type([]):
				retval =  value[0].value
			else:
				retval =  value.value
		return retval
	
	
	def getlist(self, key):
		if self.has_key(key):
			value = self[key]
			if type(value) is type([]):
				return value
			else:
				return [value]
		return []
	
		
			

class ModPythonRequest(CgiRequest):
	""" Concrete Implementation class for a mod_python Request """
	#COOKIE_KEY='Cookie'

	def req(self):
		return self._req
		
	def setup(self, handler, req): 
		#req.pso = handler
		self._req = req



	def getOutStream(self):
		return self.req()

		
	def getEnviron(self, handler): 
		self.req().add_common_vars()
		env = {}
		env.update(self.req().subprocess_env)
		env["GATEWAY_INTERFACE"] = "Python-CGI/1.1"
		if len(self.req().path_info) > 0:
			env["SCRIPT_NAME"] = self.req().uri[:-len(self.req().path_info)]
		else:
			env["SCRIPT_NAME"] = self.req().uri
		if self.req().headers_in.has_key("authorization"):
			env["HTTP_AUTHORIZATION"] = self.req().headers_in["authorization"]
		
		env.update(self.req().get_options())
		return env

	def send_http_header(self, handler, content_type='text/html'): 
		self.req().content_type =  content_type
		self.req().send_http_header() 

	def getInputs(self, handler, key=None, default=None, index=0):
		from modpython import FormInput
		return FormInput(self.req())

	def getServerReturn(self):
		return apache.SERVER_RETURN

	def getHeadersOut(self):
		return self.req().headers_out
		
	def syncHeadersOut(self, headers): pass
		#self.req().headers_out.add('cookie','MyMi')
		#for k,v in headers.flatten():
		#	self.req().headers_out.add(k,v)
		
