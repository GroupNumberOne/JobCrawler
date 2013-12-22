from Main import Main
from multiprocessing import Process, Queue, Pool
        
class StartCrawler():
    crawler_cvenv = 'http://www.cvenvacaturebank.nl'
    crawler_starapple = 'http://www.starapple.nl'
    crawler_monsterboard = 'http://www.monsterboard.nl'
    main = Main()
    def startCrawling(self,url):
        Main.start(url) 
    
    if __name__ == '__main__':
        print "Crawler started..."
        p1 = Process(target=main.start,args=(crawler_cvenv,))
        p2 = Process(target=main.start,args=(crawler_starapple,))
        p3 = Process(target=main.start,args=(crawler_monsterboard,))
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
        print "Crawler shut down."