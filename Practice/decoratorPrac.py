def one(f):
    def inner(*args, **kwargs):
        print('inner')
        return f(*args, **kwargs)
    return inner

@one
def two():
    print('two')


def three():
    print('three')


if __name__ == '__main__':
   three()

