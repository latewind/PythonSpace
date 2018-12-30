from selectors import DefaultSelector ,EVENT_WRITE
import socket

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
			next_future = self.coro.send(f.result)
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
	print('...')
	selector.unregister(sock.fileno())

class Fetcher:
	def fetch(self):
		sock = socket.socket()
		yield from connect(sock)


def loop_event():
	for key,mask in selector.select():
		callback = key.data
		callback()

selector = DefaultSelector()

fetch = Fetcher().fetch()
Task(fetch)

loop_event()


