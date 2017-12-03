#operator
#math operator
a,b,c,d=1,2,3,4
print("a+b:",a+b)
print("c-b:",c-b)
print("c*d:",c*d)
print("c/b:",c/b)
print("d%c:",d%c)
print("b**c:",b**c)
print("c//b",c//d)

#compare operator
'''
== != > < >= <=
'''

'''
= += -= /= *= **= %= //=
'''
# bit operator
a=2   #0000 0010
b=13  #0000 1101
print(a>>1) #0000 0001
print(a|b)  #0000 1111
print(a&b)  #0000 0000
print(~a)   #1111 1101
print(a^b)  #0000 1111

if a or b:
	print("or")