# pso
pso- Python Service objects is a package that simplifies HTTP handlers:  Built-in sessions. Write once run on modpython, modsnake, NASAPY, fastcgi, CGI. Easy interface to HTTP info. Simple, fast, robust and powerful extendable OO template parser.

## Introduction
We developed pso for the following reasons:
 1. We wanted to develop web systems that would work as cgi and mod_python request handlers on apache or nsapi handlers on netscape without thinking about httpd implementation details. To do this pso includes the class SerivceRequest that is a bridge between the server and any code we develop. This bridge also gives us a consistent and easy interface with the server and the client.
 2. We needed a fast and easy to use parser to extract sgml ( that includes html and xml) tags and replace them with the result of a rendered object. We also wanted to parse the templates only once and render the object tree as we needed. The pso parser if fast and simple, returning a object tree that is easily rendered or processed by a visitor pattern.
 3. We wanted to be able to just add a new tag to a template and drop in the relevant classes without changing the application code. Every tag represents an object whose class can be sub classed. You only need to place the new class in the python import path for it to be recognized and used by the parser.
 4 We found that it was only trivial systems that did not need session handling. When you use pso, session handling is available by default.
 5. We wanted lots of useful methods to handle redirection, setting cookies, targets, status, also methods to handle file uploads, and other form handling, and url coding. pso offers these.
We are programmers, so pso has been kept simple and basic. The template system offers no built in tags, you have to build your own or subclasses those contributed, by ourselves or other users. We decided on this spartan approach on the basis that by keeping pso simple and light it would be easier to maintain and keep error free. Who uses pso ? Well let us say the biggest stock market uses pso on the floor and in the back offices for there most used and important internet trading service. So will pso be maintained ? They will!




## System Requirements
 
  * Python - http://www.python.org
  * pso - http://sourceforge.net/projects/pso/


## Quick Example

Lets start with a really simple CGI:

### a `cgi` example
```python

#!/usr/bin python2.7


def testHandler():
	print "content-type: text/html"
	print
	print "hello world"

if __name__ == '__main__':	
	testHandler()

```

### A `mod_python` example

```python

from mod_python import apache

def testHandler(req):
	req.send_http_header()
	req.write( "hello world")
	return apache.OK
The above programs rewritten in pso
```


### The  above programs rewritten in `pso` that works as both a `cgi` or a `mod_python` script

```python
from pso.service import ServiceHandler

def testHandler(serviceRequest):
	print "Hello World!"  

if __name__ == '__main__':
	ServiceHandler().run(testHandler)

```
## pso.request.ServiceRequest - servicing requests

### Form Input

The ServiceRequest object has the following methods:

 * `hasInputs(self, *keys)` - tests if a field or fields in the form were filled.

 * `getInputs(self, key=None)` - which given a key will return a list of all the values associated with this key. If none exits it will return an empty list. When getInputs() is called a cgi.FieldStorage object is returned.

 * `getInput(self, key, default=None, index=None)` returns the given form field value as a string. If there are multiple values under the same key, it will return the first in the list, unless index is given. If no value is found will return `""`, unless default is given.


```python

from pso.service import ServiceHandler, OK


def testInput(serviceRequest):
	if serviceRequest.hasInput("submit"):
		name = serviceRequest.getInput("name")
		options =  ",".join(serviceRequest.getInputs("option"))
		print """<pre>
			name: %s,
			options: %s
			</pre>""" % (name, options)
	else:
		print """
			<form >
			<input name="name">
			<input name="option" value="alpha" type="checkbox">alpha
			<input name="option" value="omega" type="checkbox">omega
			<input type="hidden" name="test" value="input">
			<input type="submit" name="submit" value="submit">
			</form>
			"""
	return OK

if __name__ == '__main__':
	ServiceHandler().run(testInput)
```

### Server, request header & environment variables

pso emulates the CGI standard, and these variables are available through `ServiceRequest.getEnvrion(self, key=None, default=None)` that takes a key and either returns a string or default. If no key is given a dictionary is returned of these variables.


```python

from pso.service import ServiceHandler, OK

def testEnviron(serviceRequest):
	print "<ul>"
	for keyValue in serviceRequest.getEnviron().items():
		print "<li>%s: %s" % keyValue
	print "</ul>"
	return OK


if __name__ == '__main__':
	ServiceHandler().run(testEnviron)

```

### Handling cookies

* You get cookies using ServiceRequest.getCookies(self) that returns a dictionary of cookies and their values.
* You get a cookie using `ServiceRequest.getCookie(self, key, default=None)` which returns the cookie value requested by key otherwise returns default.
* Cookies can be set by using `setCookie(self, key, value, **attrs)` sets cookie key to value. **attrs is a key word parameter through which you can pass the cookie attributes as defined in `RCF2109`:
  * `Comment`
  * `Domain`
  * `Max-Age`
  * `Path`
  * `Secure`
  * `Version`
  * `expires`?... Used by netscape et al. This takes a string date such as `"Mon, 12 Nov 2002 13:04:56 GMT"`, as defined in RFC2068 section 3.3.1 [also RCF822 and RCF1123]

```python
from pso.service import ServiceHandler, OK

def testCookie(serviceRequest):
	if not serviceRequest.getCookie("MyTest"):
		print 'setting cookie "MyTest" to "is Tasty" reload to see this cookie'
		serviceRequest.setCookie('MyTest','is Tasty')
	print"<ul>"
	for cookieValue in serviceRequest.getCookies().items():
		print "<li>%s: %s" % cookieValue
	print "</ul>"
	return OK

 __name__ == '__main__':
	ServiceHandler().run(testCookie)
```

