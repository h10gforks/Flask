from framework import *

@controller
def hello(req):
    if req.method == 'POST':
        return 'Hello %s!' % req.params['name']
    elif req.method == 'GET':
        return '''
            <form method="POST"> 
            Your name: <input type="text" name = "name">
            <input type="submit">
            </form>
        '''
#rest controller
class Hello():
    def __init__(self, req):
        self.request = req
    def get(self):
        return '''
            <form method="POST">
            Your name: <input type="text" name="name">
            <input type="submit">
            </form>
        '''
    def post(self):
        return 'Hello %s!' % self.request.params['name']


if __name__ == '__main__':
    hello2 = rest_controller(Hello)
    hello_world = Router()
    hello_world.add_route('/', controller = hello)
    hello_world.add_route('/rest', controller = hello2)

    from paste import httpserver
    httpserver.serve(hello_world, host='127.0.0.1', port=8080)
