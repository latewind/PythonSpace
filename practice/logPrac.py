#logPrac.py
import logging

def main():
    logging.basicConfig(filename='D:/Test/myapp.log', level=logging.INFO)
    logging.info('Started')
    logging.info('Finished')

if __name__ == '__main__':
    main()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler('D:/file.log')
fh.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s-%(levelname)s-%(name)s-%(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

logger.debug('debug')
logger.info('info')

childlogger=logging.getLogger('child')
childlogger.warn('warn')
childlogger.error('error')
childlogger.critical('critical')