from functools import wraps


def decorator(count):
    def twice(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            s = [fun(*args, **kwargs) for _ in range(0, count)]
            print('inner')
            return s
        return wrapper
    return twice


@decorator(2)
def one():
    print('one')
    return 1


class Decorator:
    def __init__(self, fun):
        self._fun = fun

    def __call__(self, *args, **kwargs):
        print("Decorator fun")
        self._fun(*args, **kwargs)


@Decorator
def two():
    print("two")


if __name__ == '__main__':
    print(one())
    #two()
    
