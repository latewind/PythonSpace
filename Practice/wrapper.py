from functools import wraps

'''
模拟django中间件load过程
'''


class Zero:
    def __init__(self, func):
        self.func = func

    def __call__(self, args):
        print("before call {}".format(self))
        result = self.func(args)
        print("end call {}".format(self))
        return result


class One(Zero):
    pass


class Two(Zero):
    pass


def wrapper(func):
    @wraps(func)
    def inner(args):
        result = func(args)
        return result

    return inner


def foo(args):
    print("foo function({})".format(args))
    return args if args > 100 else 200


if __name__ == '__main__':
    handler = wrapper(foo)
    for clz in [One, Two]:
        c = clz(handler)
        handler = wrapper(c)
    print(handler(123))
