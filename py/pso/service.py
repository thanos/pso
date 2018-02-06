#
#   service.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#   licience: GPL
#   (c) thanos vassilakis 2000,2001, 2002
#
#   $Id: service.py,v 1.8 2002/05/22 02:19:54 thanos Exp $
#
__version__="$Revision: 1.8 $"

import sys
from weakref import ref
from time import time, strftime, gmtime



from util import log
from request import ServiceRequest, SERVER_RETURN
from cgirequest import CgiRequest


		
		
		



        



OK = 0
def fixup(req, requestImpl, sessionImpl=None): 
	sys.stdout = req.pso = ServiceRequest(requestImpl, req)
	session = req.pso().getSession( sessionImpl)

def cleanup(req):
	log('cleaing up', req)
	req.pso().close()


class ServiceHandler:
	PRODUCTION = 0
	def run(self, handler, sessionImpl =None ):
		try:
			stdout = sys.stdout
			stderr = sys.stderr
			sys.stdout = pso = ServiceRequest(CgiRequest)
			pso.stderr = stderr
			logfile = pso.getEnviron('PSOLog')
			if logfile:
				sys.stderr = open(logfile, 'a', 0)
			pso.session = pso.getSession( sessionImpl )
			status =  handler(pso)
		except SERVER_RETURN, status:
			pass
		except:
			sys.stdout = stdout
			import traceback
			if not self.PRODUCTION:
				traceback.print_exc(file = sys.stdout)
			else:
				traceback.print_exc()
			sys.stderr = stderr


def test(req):
	print "hello world"

def test1(req):
	print "hello world"
	req.send_http_header(content_type= 'text/plain')

def test2(req):
	print "hi there" 
	req.sendStatus(204)

def test3(req):
	print "hi there" 
	req.redirect("http://www.w3c.org/")

	
	

if __name__ =='__main__':
	ServiceHandler().run(test3)
	
		
        
