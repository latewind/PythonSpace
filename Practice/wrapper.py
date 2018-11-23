from functools import wraps

'''
模拟django中间件load过程
'''


class Zero:
    def __init__(self, func):
        self.func = func

    def __call__(self, args):
        print("before call {}".format(self.__class__))
        self.process_request(args)
        result = self.func(args)
        self.process_response(result)
        print("end call {}".format(self))
        return result

    def process_request(self, args):
        pass

    def process_response(self, response):
        pass


class One(Zero):

    def process_request(self, args):
        args.append(1)

    def process_response(self, response):
        response.append("one")


class Two(Zero):

    def process_request(self, args):
        args.append(2)

    def process_response(self, response):
        response.append("Two")


class Third(Zero):

    def process_request(self, args):
        args.append(3)

    def process_response(self, response):
        response.append("Third")


def wrapper(func):
    @wraps(func)
    def inner(args):
        result = func(args)
        return result

    return inner


def get_response(args):

    args.reverse()
    response = args.copy()
    response.append("response")
    print("foo function({})".format(response))
    return response


if __name__ == '__main__':
    handler = wrapper(get_response)
    for clz in [One, Two, Third]:
        c = clz(handler)
        handler = wrapper(c)
    print(handler(["request"]))




