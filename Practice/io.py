#fileName io.py
f=open("function.py","r")

#buf=f.read()
#print(buf)

for line in f :
	print(line,end="#")
f.close()

fw=open("io.dat","w")
fw.write("#filename io.dat\n")
fw.write("Hello Late Wind")
fw.close()
fr=open("io.dat","rb")
b=fr.readline()
print(b)
print(fr.tell())
fr.seek(-3,2)
print(fr.read())
fr.close()

#import pickle
import sys
print(sys.argv)

