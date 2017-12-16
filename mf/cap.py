# A toy framework inspired by Flask
# 先使用werkzeug来实现Cap, 之后再一步步地自己实现wsgi接口

from werkzeug import Request as BaseRequest, Response as BaseResponse, LocalStack

class Request(BaseRequest):
    #Request class
    def __init__(self, environ):
        BaseRequest.__init__(self, environ)
        self.endpoint = None

class Response(BaseResponse):
    r_mimetype = 'text/html'

def make_default_error_handlers(dic):
    for i in range(400,600):
        dic[i] = "<h1>Error:" + str(i) + "</h1>"

class Cap():

    def __init__(self):
        #一个{ rule: endpoint + ':' + methods }键值对
        #rule可以解析简单的URL参数如 <string:name> 或<int:id>
        #之后仅可返回一个静态页面
        self.url_map = {}
        
        #一个endpointname: method list键值对
        self.method_map = {}
        
        #request stack
        self.requests_stack = LocalStack()
        
        
        #a handler for 
        self.error_handlers = {}
        make_default_error_handlers(self.error_handlers)

    def route(self, rule, methods = ['GET']):
        def decorator(f):
            self.url_map[rule] = f.__name__
            self.method_map[f.__name__] = methods
            return f
        return decorator
    
    def errorhandler(self, code):
        def decorator(f):
            self.error_handler[code] = f
            return f
        return decorator

    def match_request(self):
        #匹配Rule, endpoint, methods
        #Method检查貌似是server那边做的？
        pass 
    
    def __call__(self):
        pass
