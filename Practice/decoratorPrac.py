from functools import wraps


def decorator(count):
    def twice(fun):
        @wraps(fun)
        def wraper(*args, **kwargs):
            [fun(*args, **kwargs) for _ in range(0, count)]
            print('inner')
        return wraper
    return twice


@decorator(2)
def two():
    print('two')


def three():
    print('three')


if __name__ == '__main__':
    two()
