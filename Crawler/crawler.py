#crawler.py
import socket
import re
from selectors import DefaultSelector,EVENT_WRITE
import time

def fetch():
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    print(sock)
    request = 'GET {} HTTP/1.0\r\nHost: baidu.com\r\n\r\n'.format('https://www.baidu.com/')
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    print(type(chunk))
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
    i = response.index(b'<html>')
    with open('D:/Test/baidu.html','wb') as f:
        f.write(response[i:])

def asyn_fetch():  
    selector = DefaultSelector()
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass
    selector.register(sock.fileno(),EVENT_WRITE,connected)


def connected():
    selector.unregister(sock.fileno())
    print('connected')



if __name__ == '__main__':
    selector = DefaultSelector()
    sock = socket.socket()
    sock.setblocking(False)
    try:
        time.sleep(3)
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass
    selector.register(sock.fileno(),EVENT_WRITE,connected)

    while True:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback()
