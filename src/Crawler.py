'''
JobCrawler Crawler class
Searches for and saves URL's for designated websites.
Created by Bob van Kamp & Patrick van der Reijden
'''

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

'''
If the current URL is a website of interest (containing useful information)
we store it in the database
'''    
def saveUrl(baseUrl,fullUrl,loweredfeed):
    if loweredfeed.find('cvenvacaturebank') > 0:
        if fullUrl.lower().find('/cv/koop') > 0 or fullUrl.lower().find('/cv/ideal') > 0 or fullUrl.lower().find('/vacature/doorsturen') > 0 or fullUrl.lower().find('vacature/reageer') > 0:
            return
    elif loweredfeed.find('starapple') > 0:
        if loweredfeed.find('/kandidaat-') < 0 and loweredfeed.find('-download') > 0 and loweredfeed.find('/kandidaat-tell') > 0 or loweredfeed.find('/vacature-') < 0:
            return
    
    DbHandler.insertUrl(baseUrl,fullUrl)

def crawlSite(feed):
    c=urllib2.urlopen(feed)
    soup = BeautifulSoup(c, 'lxml')
    
    DbHandler.changeDate(feed)
    loweredfeed = feed.lower()
    
    '''
    Save the good URL's that are found
    '''
    for a in soup.findAll('a'):
        if a.has_attr('href'):
            ref = a['href']
            if ref.find('http') == 0:
                saveUrl(baseUrl,a['href'],loweredfeed)
            elif ref.find('/') == 0:
                saveUrl(baseUrl,baseUrl+ref,loweredfeed)
                
    '''
    Tell a specific parser to parse the good URL's
    '''            
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
    
    '''
    See if there are URL's in the database with the feed as base.
    If not we start crawling it anew
    If there is we take these URL's and crawl them as if they are a new base URL
    '''
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
                
            '''
            Put a small delay in the crawling process in order not to flood the website with requests.
            Currently: 1.5 seconds
            Because: Developing and testing. Slower would slow down this proces.
            Plan: set to 10 seconds as a safe delay
            '''
            time.sleep(1.5)
            
            if i%50 == 0:
                DbHandler.dbCommit()
                
    DbHandler.dbCommit()
    print "Crawling complete, remaining: "+str(amount-len(feedList))
    if len(feedList) < amount and len(feedList) != 0:
        print "Continue crawling with new list ..."
        startCrawler(base, amount-len(feedList))
    
    return "Crawling completed"    