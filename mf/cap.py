# 先使用werkzeug来实现Cap, 之后再一步步地自己实现werkzeug

from werkzeug import Request as BaseRequest, Response as BaseResponse, LocalStack
from werkzeug.routing import Map, Rule

###############################################################
#################Requests And Response#########################
###############################################################

class Request(BaseRequest):
    #Request class
    def __init__(self, environ):
        BaseRequest.__init__(self, environ)
        self.endpoint = None

class Response(BaseResponse):
    response_mimetype = 'text/html'

class _RequestContext():
    def __init__(self, app, environ):
        self.app = app
        self._url_adapter = app.url_map.bind_to_environ(environ)
        self.request = app.request_class(environ)

    def __enter__(self):
        _request_ctx_stack.push(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None :
            _request_ctx_stack.pop()

###############################################################
#################     functions       #########################
###############################################################

def url_for(enpoint, **values):
    return _request_ctx_stack.top.url_adapter.build(enpoint, values)

def make_default_error_handlers(dic):
    for i in range(400,600):
        dic[i] = "<h1>Error:" + str(i) + "</h1>"


###############################################################
#################         Cap         #########################
###############################################################

class Cap():

    def __init__(self):
        #一个{ rule: endpoint + ':' + methods }键值对
        #rule可以解析简单的URL参数如 <string:name> 或<int:id>
        #之后仅可返回一个静态页面
        self.url_map = Map()

        #一个endpointname: method list键值对
        self.view_functions = {}

        #request stack
        self.requests_stack = LocalStack()
        
        
        #a handler for 
        self.error_handlers = {}
        make_default_error_handlers(self.error_handlers)


    def run(self, host = 'localhost', port = 2000):
        from werkzeug import run_simple
        return run_simple(host, port, self)

    def route(self, rule, methods = ['GET']):
        def decorator(f):
            self.add_url_rule(rule, f.__name__, methods)
            self.view_functions[f.__name__] = methods
            return f
        return decorator

    def add_url_rule(self, rule, endpoint, methods):
        options = {
            'endpoint': endpoint,
            'methods': methods
        }
        _rule = Rule(rule, options)
        self.url_map.add(_rule)

    def errorhandler(self, code):
        def decorator(f):
            self.error_handlers[code] = f
            return f
        return decorator

    def match_request(self):
        #匹配Rule, endpoint, methods
        #Method检查貌似是server那边做的？
        pass


    def wsgi_app(self, environ, start_response):
        pass

    def __call__(self):
        pass


###############################################################
#################       globals       #########################
###############################################################

_request_ctx_stack = LocalStack()