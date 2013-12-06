import psycopg2
import psycopg2.extras
import urllib2
from bs4 import BeautifulSoup
import time
import Parsers.CVenVParser as CVenVParser
import DbHandler as DbHandler

baseUrl = '';
    
def saveUrl(baseUrl,fullUrl):
    if fullUrl.lower().find('/cv/koop') > 0 or fullUrl.lower().find('/cv/ideal') > 0 or fullUrl.lower().find('/vacature/doorsturen') > 0 or fullUrl.lower().find('vacature/reageer') > 0:
        return
    
    DbHandler.insertUrl(baseUrl,fullUrl)
 
def crawlSite(feed):
    c=urllib2.urlopen(feed)
    soup = BeautifulSoup(c, "lxml")
    for a in soup.findAll('a'):
        if a.has_attr('href'):
            ref = a['href']
            if ref.find('http') == 0:
                saveUrl(baseUrl,a['href'])
            elif ref.find('/') == 0:
                saveUrl(baseUrl,baseUrl+ref)
                
    DbHandler.changeDate(feed)
    loweredfeed = feed.lower()
    if loweredfeed.find('cvenvacaturebank') > 0 and loweredfeed.find('/cv/') > 0 and loweredfeed.find('/koop/') < 0 and loweredfeed.find('/ideal/') < 0 and loweredfeed.find('.html') > 0:
        CVenVParser.parseCV(soup,feed)
    elif loweredfeed.find('cvenvacaturebank') > 0 and loweredfeed.find('/vacature/') > 0 and loweredfeed.find('.html') > 0 and loweredfeed.find('/reageer/') < 0 and loweredfeed.find('/doorsturen/') < 0:
        CVenVParser.parseVacature(soup,feed)
            
def startCrawler(base,amount=20):
    print "Crawler started for "+str(amount)+" crawls"
    global baseUrl
    baseUrl = base
    
    feedList = DbHandler.gatherUrls(base,amount)
    i = 1;
    
    if not feedList:
        crawlSite(base)
    else:
        for feed in feedList:
            print "Crawling "+str(i)+" of "+str(amount)
            try:
                crawlSite(feed['fullurl'])
            except:
                print "Could not crawl "+feed['fullurl']
            time.sleep(2)
            i+= 1
            if i%10 == 0:
                DbHandler.dbCommit()
    
    #Select some urls from the database and crawl those sites. Finally, commit the changes.
    DbHandler.dbCommit()
    
    if len(feedList) < amount and len(feedList) != 0:
        startCrawler(base, amount-len(feedList))
    print "Crawling complete"