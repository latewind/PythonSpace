from functools import wraps


def decorator(count):
    def twice(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            [fun(*args, **kwargs) for _ in range(0, count)]
            print('inner')

        return wrapper

    return twice


@decorator(2)
def one():
    print('two')


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
    one()
    two()
