#logMultProcess.py
#--*-- uft-8 --*--
import multiprocessing
from multiprocessing import Pool,Queue,Process
import logging
from logging import handlers
import random
import time
import threading
def configure_lsnr():
	root = logging.getLogger()
	fh = handlers.RotatingFileHandler('D:/Test/review6.log','a',500)
	formatter = logging.Formatter('%(asctime)-10s-%(name)-10s-%(processName)-10s-%(message)-10s')
	fh.setFormatter(formatter)
	root.addHandler(fh)
def run_listener(q,config): 
	config()
	while True :
		record = q.get()
		if record is None :
			print("None")
			break
		logger = logging.getLogger(record.name)
		logger.handle(record)
	

def configure_worker(q):
	root = logging.getLogger()
	qh = handlers.QueueHandler(q)
	root.addHandler(qh)

levels = [logging.DEBUG,logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL]
loggers = ['a','b','c']

def run_worker(q,config):
	config(q)
	for _ in range(0,10):
		logger = logging.getLogger(random.choice(loggers))
		logger.log(random.choice(levels),'message %d',_)
		time.sleep(0.1)

def main():
	queue = multiprocessing.Manager().Queue(-1)
	lsnr=threading.Thread(target=run_listener,args=(queue,configure_lsnr))
	lsnr.start()
	works=[]
	for _ in range(0,5):
		worker=Process(target=run_worker,args=(queue,configure_worker))
		worker.start()
		works.append(worker)

	for worker in works:
		worker.join()

	queue.put_nowait(None)

	lsnr.join()
if __name__ == '__main__':
	main()

