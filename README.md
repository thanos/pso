# pso
`pso`- Python Service objects is a package that simplifies HTTP handlers:  Built-in sessions. Write once run on modpython, modsnake, NASAPY, fastcgi, CGI. Easy interface to HTTP info. Simple, fast, robust and powerful extendable OO template parser.

## Introduction
We developed `pso` for the following reasons:
 1. We wanted to develop web systems that would work as cgi and mod_python request handlers on apache or nsapi handlers on netscape without thinking about httpd implementation details. To do this `pso` includes the class SerivceRequest that is a bridge between the server and any code we develop. This bridge also gives us a consistent and easy interface with the server and the client.
 2. We needed a fast and easy to use parser to extract sgml ( that includes html and xml) tags and replace them with the result of a rendered object. We also wanted to parse the templates only once and render the object tree as we needed. The `pso` parser if fast and simple, returning a object tree that is easily rendered or processed by a visitor pattern.
 3. We wanted to be able to just add a new tag to a template and drop in the relevant classes without changing the application code. Every tag represents an object whose class can be sub classed. You only need to place the new class in the python import path for it to be recognized and used by the parser.
 4 We found that it was only trivial systems that did not need session handling. When you use `pso`, session handling is available by default.
 5. We wanted lots of useful methods to handle redirection, setting cookies, targets, status, also methods to handle file uploads, and other form handling, and url coding. `pso` offers these.
We are programmers, so `pso` has been kept simple and basic. The template system offers no built in tags, you have to build your own or subclasses those contributed, by ourselves or other users. We decided on this spartan approach on the basis that by keeping `pso` simple and light it would be easier to maintain and keep error free. Who uses `pso` ? Well let us say the biggest stock market uses `pso` on the floor and in the back offices for there most used and important internet trading service. So will `pso` be maintained ? They will!




## System Requirements
 
  * Python - http://www.python.org
  * pso - http://sourceforge.net/projects/`pso`/


## Quick Example

Lets start with a really simple CGI:

### a `cgi` example
```python

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
```

### The  above programs rewritten in `pso` that works as both a `cgi` or a `mod_python` script

```python
from pso.service import ServiceHandler

def testHandler(serviceRequest):
	print ('Hello World!') 

if __name__ == '__main__':
	ServiceHandler().run(testHandler)

```
## `pso.request.ServiceRequest` - servicing requests

### Form Input

The `ServiceRequest` object has the following methods:

 * `hasInputs(self, *keys)` - tests if a field or fields in the form were filled.

 * `getInputs(self, key=None)` - which given a key will return a list of all the values associated with this key. If none exits it will return an empty list. When `getInputs()` is called a `cgi.FieldStorage` object is returned.

 * `getInput(self, key, default=None, index=None)` returns the given form field value as a string. If there are multiple values under the same key, it will return the first in the list, unless index is given. If no value is found will return `""`, unless default is given.


```python

from pso.service import ServiceHandler, OK


def testInput(serviceRequest):
	if serviceRequest.hasInput("submit"):
		name = serviceRequest.getInput("name")
		options =  ",".join(serviceRequest.getInputs("option"))
		print ("""<pre>
			name: %s,
			options: %s
			</pre>""") % (name, options)
	else:
		print ("""
			<form >
			<input name="name">
			<input name="option" value="alpha" type="checkbox">alpha
			<input name="option" value="omega" type="checkbox">omega
			<input type="hidden" name="test" value="input">
			<input type="submit" name="submit" value="submit">
			</form>
			""")
	return OK

if __name__ == '__main__':
	ServiceHandler().run(testInput)
```

### Server, request header & environment variables

`pso` emulates the `CGI` standard, and these variables are available through `ServiceRequest.getEnvrion(self, key=None, default=None)` that takes a key and either returns a string or default. If no key is given a dictionary is returned of these variables.


```python

from pso.service import ServiceHandler, OK

def testEnviron(serviceRequest):
	print ('<ul>')
	for keyValue in serviceRequest.getEnviron().items():
		print ('<li>%s: %s' % keyValue)
	print ('</ul>')
	return OK


if __name__ == '__main__':
	ServiceHandler().run(testEnviron)

```

### Handling cookies

* You get cookies using `ServiceRequest.getCookies(self)` that returns a dictionary of cookies and their values.
* You get a cookie using `ServiceRequest.getCookie(self, key, default=None)` which returns the cookie value requested by key otherwise returns default.
* Cookies can be set by using `setCookie(self, key, value, **attrs)` sets cookie key to value. **attrs is a key word parameter through which you can pass the cookie attributes as defined in [`RCF 2109`](https://www.ietf.org/rfc/rfc2109.txt):
  * `Comment`
  * `Domain`
  * `Max-Age`
  * `Path`
  * `Secure`
  * `Version`
  * `expires`?... Used by netscape et al. This takes a string date such as `"Mon, 12 Nov 2002 13:04:56 GMT"`, as defined in [`RFC 2068`](https://www.ietf.org/rfc/rfc2068.txt) section 3.3.1 [also [`RCF 822`](https://www.ietf.org/rfc/rfc822.txt) and [`RCF 1123`](https://www.ietf.org/rfc/rfc1123.txt)

```python
from pso.service import ServiceHandler, OK

def testCookie(serviceRequest):
	if not serviceRequest.getCookie("MyTest"):
		print ('setting cookie "MyTest" to "is Tasty" reload to see this cookie')
		serviceRequest.setCookie('MyTest','is Tasty')
	print ('<ul>')
	for cookieValue in serviceRequest.getCookies().items():
		print ('<li>%s: %s' % cookieValue)
	print ('</ul>')
	return OK

 __name__ == '__main__':
	ServiceHandler().run(testCookie)
```

### File Uploads

`pso` makes file uploading very easy. It offers the method `ServiceRequest.getFile(self, key)` that returns a PSOFields object, a subclass of `cgi.Field`. The return object has all some additional member fields:
 * `filename` - the original file's name
 * `file` - a file object holding the actual file
 * `tempname` - is None until the member method keep() is called.

The returned fields object has also some new methods:
 * `keep()` - For each uploaded file the python standard cgi library opens a temporary file and immediately deletes (unlinks) it. The trick (on Unix!) is that the file can still be used, but it can't be opened by any other process, and it will automatically be deleted when it is closed or when the current process terminates. keep() gives this temporary a new temporary name. This is especially useful for forms that have a confirmation screen.
 * `save(pathName)` - renames an uploaded file.


```python
import os

def testUpload(serviceRequest):
	if serviceRequest.hasInputs('file'):
		file = serviceRequest.getFile('file')
		file.keep()
		print ("""
		<form >
			Save As: <input name="saveAs" type="text" >
			<input name="tempfile" type="hidden" value="%s">
			<input name="test" type="hidden" value="upload">
		</form> """ % file.tempname)

	elif serviceRequest.hasInputs('saveAs'):
		tempFile = serviceRequest.getInput('tempfile')
		saveAs = serviceRequest.getInput( 'saveAs')
		
		print ("renaming", tempFile, 'to', '/tmp/'+saveAs)
		os.rename(tempFile, '/tmp/'+saveAs)
		print ("""
		DONE - Thankyou
		""")
	else:
		print ("""
			<form  enctype="multipart/form-data" method="POST">
			file: <input name="file" type="file" >
			<input name="test" type="hidden" value="upload">
			<input name="action" type="submit" value="Upload">
		</form>""")
	return OK


if __name__ == '__main__':
	ServiceHandler().run(testUpload)

```

### Redirection

Redirection is essential and `pso` makes this easy. Just call `ServiceRequest.redirect(someUrl)` and your script will terminate and redirect the client's browser.

```python
from pso.service import ServiceHandler,OK

def testRedirect(serviceRequest):
	url =  serviceRequest.getInput('url')
	if not url:
		print ("""
		<form >
		Redirect to : <input name="url" type="text" size=40">
		<input name="test" type="hidden" value="redirect">
		</form>""")
	else:
		serviceRequest.redirect(url)
	return OK



if __name__ == '__main__':
	ServiceHandler().run(testRedirect)
```


### Status

By default `pso` always sets the return status to `200`. When invoking redirect, pso will set the status code to either `301` or `302`. To set the code explicitly you have a choice of invoking:
 * `sendStatus(self, status)` - this immediately sends the status code and terminates you handler.
 * `setStatus(self, status)` - this sets the status code but your request handler will continue execution.
For a complete list of these codes you should refer to [`rfc2616 sec6.1.1`](https://tools.ietf.org/html/rfc2616#section-6.1).

```python
from pso.service import ServiceHandler,OK

def testStatus(serviceRequest):
	if not serviceRequest.hasInput('status'):
		print ("""
		<form>
			<input name="status" type="text" size=3" maxsize=3>
			<input name="test" type="hidden" value="status">
		</form>""")
	else:
		status = serviceRequest.getInput('status', '204')
		serviceRequest.sendStatus(status)
	return OK

if __name__ == '__main__':
	ServiceHandler().run(testRedirect)
```



### Target and other http headers

`pso` sets many headers `(status, content_type, cookie)`, and it is easy to do using :
 * `setHeaderOut(self, key, value)` - replaces the header entry with the same key.
 * `addHeaderOut(self, key, value)` - adds the header entry.


```python
from pso.service import ServiceHandler,OK

def testHeaderOut(serviceRequest):
	if serviceRequest.hasInputs('url','target'):
		serviceRequest.setHeaderOut('Window-target', serviceRequest.getInput('target'))
		print ('<ul>')
		table = serviceRequest.getHeadersOut()
		for k in table.keys(): 
			print ('<li>',k, table[k])
		print ('</ul>')
		print serviceRequest.getInput('message')
	else:		
		print ("""
		WIndow target seems to only work with netscape, please try and let us know.
		<form>
			target: <input name="target" type="text" > 
			message: <input name="message" type="text" size=50 > 
			<input type="hidden" name="test" value="headerOut">
			<input name="action"  type="submit" value="write to target"> 
		</form>""")


 __name__ == '__main__':
	ServiceHandler().run(testHeaderOut)
```


### sys.stdout

When using `psosys.stdout` is buffered until the termination of the request handler or the invocation of `ServiceRequest.send_http_header( self, content_type='text/html')`. This system allows you to use print without worrying about when you set the headers, cookies or when you what to redirect. Buffering can damage a performance on very large return screens, yet it can simplify the program logic, and in most cases web services try to fit their return results on one screen. When you want top stop buffering just send the headers, using the method `send_http_header`. If you want write directly to the `sys.stdout` before sending the headers you can use:

```python
requestService.write(someString)
```

sys.stderr and logging
By default the output to sys.stderr is posted to the httpd log, but this can be easily changed using the following httpd directive:
CGI	mod_python
SetEnv PSOLog=/path/to/some/Log
PythonOption PSOLog=/path/to/some/Log
pso.ServiceRequest also has a member function log(self, *listToPost) that will post a line to the log starting with a timestamp then followed by the parameters in listToPost.
