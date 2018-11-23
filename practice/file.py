 #filename file.py
 #f=open("io.py","r")
with open("function.py","r") as f:
	for index in range(5):
		print(next(f),end=str(index))