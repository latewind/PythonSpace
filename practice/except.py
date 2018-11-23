#exception
try:
	result=1/0
except ZeroDivisionError:
	print("error")
else:
	print("other")

class RaiseError(Exception):
	def __int__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)
try:
	raise RaiseError
except RaiseError:
	print("catch RaiseError")
finally:
	print("finally")