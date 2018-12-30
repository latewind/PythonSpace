list=["late","wind","2017","6.4"]
tinylist=["good","day"]
print(list)
print(list[2:])
print(list[1:3])
print(list[1:-2])
print(list[0])
print(list+tinylist)
del list[0]
print(list[0])
print(len(list))
listCompose=list+tinylist;
listCompose.append('I am OK')
listCompose.sort()
sub=['sub1','sub2']
listCompose.append(sub)
print(listCompose)
print(listCompose[-3:])
print(listCompose[-1][0])

import sys
it=iter(listCompose)
#for v in it:
while True:
	try:
		print (next(it))
	except StopIteration:
		sys.exit()