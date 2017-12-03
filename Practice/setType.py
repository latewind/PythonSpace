student={'Tom','Jim','Mery','Tom'}
print(student)
if('Tom' in student):
	print("exist Tom")
else :
	print("non exist Tom")

a = set('abcdeedcbar')
b = set('abcp')
print(a)
print(a-b)
print(a | b)
print( a & b)
print(a ^ b)