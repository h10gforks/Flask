from cap import Cap

capper = Cap()

@capper.route('/test/')
def test():
    print('test')

if __name__ == '__main__':
    pass
