list=[1,2,3,4]
print(list)
list.append(5)
list.reverse()
list.sort()
list.pop()
print(list)

xlist=[x**x for x in list]
print(xlist)

maxrix=[
		[1,2,3,4],
		[21,22,23,24],
		[31,32,33,34]
	]
remaxrix=[[row[i] for row in maxrix ] for i in range(4)]
del remaxrix[0]
print (remaxrix)
a={1,2,3,4,5,11,12}
b={1,2,3,4,5,21,22}
print(a|b)
print(a&b)
print(a^b)
print(a-b)

dict={2:"two",3:"three",4:"four"}
print(dict)
dictX={x:x**2 for x in list}
print(dictX)

for k,v in dict.items():
	print(k,v)