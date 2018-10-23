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

