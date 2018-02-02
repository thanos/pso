#
#   $RSCFile$  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: util.py,v 1.4 2002/04/11 22:29:29 thanos Exp $
#
__version__="$Revision: 1.4 $"

import time
class Log:
	def __init__(self, path=None):
		self.logfile = path
	def log(self, *args):
		args = map(str, args)
		post = "\n%s: %s" % ( time.ctime(), ' '.join(args))
		try:
			open(self.logfile,'a').write(post)
		except:
			import traceback
			traceback.print_exc()
import os
logger=Log(os.environ.get('PSOLOG','/tmp/test.log'))
log = logger.log
		

class MixIn:
	def getDirectives(self, objclass, reqHandler):
		directives ={}
		for key in objclass.DIRECTIVES: 
			lkey = objclass.DIRECTIVEtAG + key
			value = reqHandler.getEnviron( lkey)
			if value:
				directives[key] = value
		return directives

def mkDict(**kv):
	return kv

def get(dict,key, default=None):
	if dict.has_key(key):
		return dict[key]
	return default



