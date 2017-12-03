import sys



for i in sys.path:
	print(i)

print(sys.path)

import stringType

from function import calcuArea 
getArea=calcuArea
area=getArea(2,10)
print(area)
