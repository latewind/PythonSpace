def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('consumer n-->%s' % n)


def produce(c):
    c.send(None)
    n = 5
    while n:
        c.send(n)
        print('produce n-->%s' %n)
        n = n - 1
    c.close()

c = consumer()
produce(c)