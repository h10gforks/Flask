import re
import sys
import threading
import urllib
import os
import tempita

from webob import Request, Response
from webob import exc

var_regex = re.compile(r'''
    \{
    (\w+)
    (?::([^}]+))?
    \}
''', re.VERBOSE)

def template_to_regex(template):
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex

def load_controller(string):
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func

class Router():
    def __init__(self):
        self.routes = []
    
    def add_route(self, template, controller, **vars):
        if isinstance(controller, type("")):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template)),
                            controller,
                            vars))
    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)

#wrapper make a function to a controller
def controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException as e:
            resp = e
        if isinstance(resp, type("")):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement

#restful controller
#cls is shorten  fron class
def rest_controller(cls):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            instance = cls(req, **req.urlvars)
            action = req.urlvars.get('action')
            if action:
                action += '_' + req.method.lower()
            else:
                action = req.method.lower()
            
            try:
                method = getattr(instance, action)
            except AttributeError:
                raise exc.HTTPNotFound("No action %s" % action)

            resp = method()
            if isinstance(resp, type("")):
                resp = Response(body=resp)
        except exc.HTTPException as e:
            resp = e
        return resp(environ, start_response)
    return replacement

'''
We can use thread-local variables to make it easy for any function to get access to the current request. 
A "thread-local" variable is a variable whose value is tracked separately for each thread
so if there are multiple requests in different threads
their requests won't clobber each other.
'''
class Localized(object):
    def __init__(self):
        self.local = threading.local()

    def register(self, object):
        self.local.object = object

    def unregister(self):
        del self.local.object

    def __call__(self):
        try:
            return self.local.object
        except AttributeError:
            raise TypeError("No object has been registered for this thread.")

get_request = Localized()

#middleware to register the request object. 
class RegisterRequest():
    def __init__(self, app):
        self.app = app
    #__call__ is special method used when u use a object as a func
    def __call__(self, environ, start_response):
        req = Request(environ)
        get_request.register(req)
        try:
            return self.app(environ, statr_response)
        finally:
            get_request.unregister()

#URL Generation
def url(*segments, **vars):
    #application_url is the attribute belongs to threading.local().application_url
    base_url = get_request().application_url
    path = '/'.join(str(s) for s in segments)

    if not path.startswith('/'):
        path = '/' + path
    
    if vars:
        path += '?' + urllib.urlencode(vars)
    return base_url + path

#template
def render(template, **vars):
    if isinstance(template, type("")):
        caller_location = sys._getframe(1).f_globals['__file__']
        filename = os.path.join(os.path.dirname(caller_location), template)
        template = tempita.HTMLTemplate.from_filename(filename)
    vars.setdefault('request', get_request())
    return template.substitute(vars)
