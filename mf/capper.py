from cap import Cap

capper = Cap()

@capper.route('/test/', methods = ['GET', 'POST'])
def test():
    print('test')

if __name__ == '__main__':
    capper.run()
