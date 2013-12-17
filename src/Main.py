#import Crawler
import time
from multiprocessing import Process

class Main(Process):
    urlToCrawl = ''
    crawling = False
    
    def __init__(self,url):
        global urlToCrawl
        urlToCrawl = url
                
    def start(self,url):
        global urlToCrawl
        print urlToCrawl
        print url
        
    def printen(self,url):
        print url
    
    def idle(self):
        global crawling
        while not crawling:
            #Check if we can crawl
                #if yes, break.
            time.sleep(1800)