# multProcessPrac.py
from multiprocessing import Process,Lock,Value
import time
import os
def f(name,num,lock):
		while True :
			with lock :
				 wwif num.value :
					print('hello',name,os.getpid(),num.value)
					num.value -= 1
				else :
					break 
			time.sleep(1)
					
if __name__ == '__main__' :
	count = Value('i',100) 
	lock=Lock()
	p1 = Process(target=f,args=('Tom',count,lock))
	p1.start()
	p2 = Process(target=f,args=('Jimmy',count,lock))
	p2.start()
	p3 = Process(target=f,args=('Lucy',count,lock))
	p3.start()
	p4 = Process(target=f,args=('Andy',count,lock))
	p4.start()
	p5 = Process(target=f,args=('lily',count,lock))
	p5.start()
