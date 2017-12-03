def calcuArea(width,height):
	return width*height

area=calcuArea(10,8)
print(area)

areaReverse=calcuArea(height=80,width=90)
print(areaReverse)

def defaultArg(arg=10):
	print(arg)
defaultArg()
defaultArg(20)


def varArgs(no,*args):
	for arg in args:
		print(arg)
varArgs(10,1,2,3,4,5)

#lambda
sum=lambda arg1,arg2:arg1+arg2
print(sum(1,2))