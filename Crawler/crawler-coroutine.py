from selectors import DefaultSelector ,EVENT_WRITE ,EVENT_READ
import socket
import re
from html.parser import HTMLParser
class Future:
    def __init__(self):
        self.result = None
        self._callback = []
    def add_callback(self,fn):
        self._callback.append(fn)
    def set_result(self,result):
        self.result = result
        for fn in self._callback:
            fn(self)
    def __iter__(self):
        yield self
        return self.result

class Task:
    def __init__(self,coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)
    def step(self,f):
        try :
            next_future = next(self.coro)
        except StopIteration:
            return
        next_future.add_callback(self.step)


def connect(sock):
    sock.setblocking(False)
    f = Future()
    try:
        sock.connect(('www.baidu.com',80))
    except BlockingIOError :
        pass
    def on_connected():
        print('connected',sock)
        f.set_result(None)
    selector.register(sock.fileno(),EVENT_WRITE,on_connected)
    yield from f
    selector.unregister(sock.fileno())

def read(sock):
    f = Future()
    def on_readabled():
        ret=sock.recv(4096)
        f.set_result(ret)
    selector.register(sock.fileno(),EVENT_READ,on_readabled)
    chunk = yield from f
    selector.unregister(sock.fileno())
    return chunk

def read_all(sock):
    chunk = yield from read(sock)
    response=[]
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)
    return b''.join(response)

class Fetcher:
    def __init__(self,url):
        self.response = b''
        self.url = url
    def fetch(self):

        sock = socket.socket()
        yield from connect(sock)
        get = 'GET {} HTTP/1.0\r\nHost: baidu.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))
        self.response = yield from read_all(sock)
        self._process_response()
    def _process_response(self):
        urls=re.findall(b'href="(.*?)"',self.response)
        print(urls,'*****************',self.url) 
        for url in urls:
            try:
                r=re.search(b'(?<=//www.baidu.com).*',url).group(0)            
            except Exception :
                continue
            Task(Fetcher(r.decode()).fetch())
        
def loop_event():
    while True:
        for key,mask in selector.select():
            callback = key.data
            callback()

selector = DefaultSelector()

fetch = Fetcher('/').fetch()
Task(fetch)

loop_event()


