from Crawler import Crawler
import time
from multiprocessing import Process
from DbHandler import DbHandler

class Main(Process):
    urlToCrawl = ''
    crawling = False
    crawler = None
    db = DbHandler()
    
    def __init__(self,url=None):
        global urlToCrawl
        if url is not None:
            urlToCrawl = url
                
    def start(self,url):
        global urlToCrawl,crawler
        urlToCrawl = url
        Main.crawler = Crawler()
        self.idle()
        
    def printen(self,url):
        print url
    
    def idle(self):
        while not Main.crawling:
            status = self.db.getCrawlstate(urlToCrawl)
            if status[0]:
                Main.crawling = True
            else:
                time.sleep(1800)
        Main.crawling = False
        Main.crawler.startCrawler(urlToCrawl,status[1])