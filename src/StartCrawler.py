from Main import Main
from multiprocessing import Process, Queue, Pool
        
class StartCrawler():
    crawler_cvenv = 'http://www.cvenvacaturebank.nl'
    crawler_starapple = 'http://www.starapple.nl'
    crawler_monsterboard = 'http://www.monsterboard.nl'
    #main = Main()
    def startCrawling(self,url):
        Main.start(url)
        
    main = Main(crawler_cvenv)    
    
    if __name__ == '__main__':
        p1 = Process(target=main.start,args=('woop',))
        p2 = Process(target=main.start,args=('droop',))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
