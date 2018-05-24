#
#   handlers.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: handlers.py,v 1.2 2002/05/25 00:33:10 thanos Exp $
#
__version__="$Revision: 1.2 $"

from service import OK
from parser import CachedParser


class TemplateHandler:
	TMPL="%s.html" 
	TMPL_PATH='templates/'
	def renderer(self, object, cdata=''):
		if object:
			return object(self, cdata)
		return cdata	

	def parse(self, req):
		self._req = req
		self._scratch={}
		template = self.buildTemplate(self.req())
		tree = CachedParser().parseFile(template)
		html =  tree.render(self.renderer) 
		self._req = None
		return html

	def handle(self, req):
		print self.parse(req)
		return OK

	def req(self):
		return self._req

	def scratch(self):
		return self._scratch
	


	def buildTemplate(self, req):
		return self.TMPL_PATH+self.TMPL % self.getTemplate(req)
		
	def getTemplate(self, req):
		return req.pso().getEnviron('PATH_INFO', self.getDefaultTemplate(req))

	def getDefaultTemplate(self, req):
		if not hasattr(self, 'DEFAULT_TEMPLATE'):
			raise 'please either define attribute DEFAULT_TEMPLATE or override %s' % self.getDefaultTemplate
		return self.DEFAULT_TEMPLATE
