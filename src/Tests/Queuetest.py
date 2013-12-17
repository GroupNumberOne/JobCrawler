import time
import Queue
from multiprocessing import Process, Queue, Pool
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from Crawler import Crawler

def mult(x=3):
    print time.time()
    for i in xrange(10000000): pass
    print "end: "+str(time.time())

if __name__ == '__main__':
    p1 = Process(target=Crawler.startCrawler,args=('http://www.starapple.nl',3))
    p2 = Process(target=Crawler.startCrawler,args=('http://www.cvenvacaturebank.nl',))
    print time.time()
    p1.start()
    p2.start()
    #p1.join()
    #p2.join()