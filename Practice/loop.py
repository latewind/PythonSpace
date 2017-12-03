n=100
sum=0
while n>0:
	sum=sum+n
	n-=1;
print (sum)
n=0
# loop condition
while n<5:
	print(n)
	n+=1
else:
	print("n gt 5")

# for stament
list=['1','2','3']
for v in list:
	print (v)
else :
	print("end for loop") 
print("v:",v)
#break
m=100
while m>0:
	m-=1
	if m==80:
		pass
		print("continue:",m)
		continue
print("m=",m) 