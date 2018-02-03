#
#   tags.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: tags.py,v 1.6 2002/06/03 15:52:29 thanos Exp $
#
from parser import Tag
from handlers import TemplateHandler
import sys
from cStringIO import StringIO


class Template(Tag, TemplateHandler):
	FIELD_NAME='action'

	def getTemplate(self, req):
		return req.getInput(self.FIELD_NAME, self.getDefaultTemplate(req))
		
	def __call__(self, handler, cdata=''):
#		return self.getTemplate( handler.req())
		return self.parse(handler.req())

	def getDefaultTemplate(self, req):
		default = self.attrs.get('default')
		if not default:
			raise 'please set tag attribute default or override me %s' % self.getDefaultTemplate
		return default


class Exec(Tag):
	def __call__(self, handler, cdata=''):
		if not cdata:
			return ''
		oldout = sys.stdout
		try:
			sys.stdout = StringIO()
			exec cdata
			retval = sys.stdout.getvalue()
			sys.stdout.close()
		finally:
			sys.sdtout = oldout
		return retval	
		
class DataMixin:		
	KEY=None
	def getKey(self, handler): 
		return handler.req().getInput(self.KEY) 

	def getRecord(self, handler, key): pass

	def record(self, handler): 
		key = self.getKey(handler)
		if key:
			scratchKey = (self.DATAMODEL, key)
			record = handler.scratch().get(scratchKey)
			if not record:
				record = self.getRecord(handler, key)
				if record:
					handler.scratch()[scratchKey] = record
			return record
			
		
	def getSelect(self, handler): pass
		
	def getSelection(self, handler, select): pass

	
		
	def selection(self, handler): 
		criteria = self.getSelect(handler)
		scratchKey = (self.DATAMODEL, 'select')
		cursor = handler.scratch().get(scratchKey)
		if not cursor:
			cursor = self.getSelection(handler, criteria)
			if cursor:
				handler.scratch()[scratchKey] = cursor
			return cursor
		
		
		
		
	
		
