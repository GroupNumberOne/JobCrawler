import psycopg2
import psycopg2.extras
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime,date
import time
import Parsers.CVenVParser as CVenVParser
import Parsers.SAParser as SAParser
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
    if loweredfeed.find('cvenvacaturebank') > 0:
        if loweredfeed.find('/cv/') > 0 and loweredfeed.find('/koop/') < 0 and loweredfeed.find('/ideal/') < 0 and loweredfeed.find('.html') > 0:
            CVenVParser.parseCV(soup,feed)
        elif loweredfeed.find('/vacature/') > 0 and loweredfeed.find('.html') > 0 and loweredfeed.find('/reageer/') < 0 and loweredfeed.find('/doorsturen/') < 0:
            CVenVParser.parseVacature(soup,feed)
    elif loweredfeed.find('starapple') > 0:
        if loweredfeed.find('/kandidaat-') > 0 and loweredfeed.find('-download') < 0 and loweredfeed.find('/kandidaat-tell') < 0:
            SAParser.parseCV(soup,feed)
        elif loweredfeed.find('/vacature-') > 0:
            SAParser.parseVacature(soup,feed)
            
def startCrawler(base,amount=40):
    global baseUrl
    baseUrl = base
    start_time = time.time()
    feedList = DbHandler.gatherUrls(base,amount)
    print "Crawler started for "+str(amount)+" crawls with a list of "+str(len(feedList))
    i = 1;
    
    if not feedList:
        try:
            crawlSite(base)
        except:
            print "Could not crawl "+base
    else:
        for feed in feedList:
            print "Crawling "+str(i)+" of "+str(amount)+" ("+feed['fullurl']+")"
            print "Est. time until completion: "+str(round((time.time()-start_time)/i*(amount-i)/60))+"m"
            try:
                crawlSite(feed['fullurl'])
            except:
                print "Could not crawl "+feed['fullurl']
            time.sleep(1.5)
            i+= 1
            if i%50 == 0:
                DbHandler.dbCommit()
                
    DbHandler.dbCommit()
    print "Crawling complete, remaining: "+str(amount-len(feedList))
    if len(feedList) < amount and len(feedList) != 0:
        print "Continue crawling with new list ..."
        startCrawler(base, amount-len(feedList))
    