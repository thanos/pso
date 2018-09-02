#
#   table.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: table.py,v 1.4 2002/05/28 04:10:10 thanos Exp $
#
__version__="$Revision: 1.4 $"
from types import ListType

try:
	mapClass = dict
except:
	import UserDict 
	mapClass = UserDict.UserDict

class Table(mapClass):
	def add(self, key, value):
		try:
			self[key.lower()].append(value)
		except:
			self[key.lower()] = [value]

	def set(self, key, value):
		self[key.lower()] = [value]

	def __repr__(self):
		text=""
		for k, v in self.flatten():
				text += "%s: %s\n" % ( k,v)
		return text

	def flatten(self):
		items=[]
		for key, values in self.items():
			if type(values) is ListType:
				for value in values:
					items.append((key,value))
			else:
				items.append((key,values))
		return items

class CIMap(mapClass):
	def __setitem__(self, key, item):
		mapClass.__setitem__(self, key.lower(), item)
	
		
				

if __name__ =='__main__':
	print Table.__bases__
	t = Table()
	t.add("cookie-set","me")
	t.add("cookie-set","you")
	t.add("max-set","1")
	t.set("max-set","2")
	print t
	
		
