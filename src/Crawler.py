'''
JobCrawler Crawler class
Searches for and saves URL's for designated websites.
Created by Bob van Kamp & Patrick van der Reijden
'''

import psycopg2
import psycopg2.extras
import urllib2
import sys
from bs4 import BeautifulSoup
import time
from Parsers.MBParser import MBParser
from Parsers.CVenVParser import CVenVParser
from Parsers.SAParser import SAParser
from DbHandler import DbHandler


class Crawler:    
    
    baseURL = ''
        
    sap = SAParser()
    cvvp = CVenVParser()
    mbp = MBParser()
            
    db = DbHandler()
    
    '''
    If the current URL is a website of interest (containing useful information)
    we store it in the database
    '''    
    def saveUrl(self,baseUrl,fullUrl,loweredfeed):
        if loweredfeed.find('cvenvacaturebank') > 0:
            if fullUrl.lower().find('/cv/koop') > 0 or fullUrl.lower().find('/cv/ideal') > 0 or fullUrl.lower().find('/vacature/doorsturen') > 0 or fullUrl.lower().find('vacature/reageer') > 0:
                return
        elif loweredfeed.find('starapple') > 0:
            if loweredfeed.find('/kandidaat-') < 0 and loweredfeed.find('-download') > 0 and loweredfeed.find('/kandidaat-tell') > 0 or loweredfeed.find('/vacature-') < 0:
                return
            
        self.db.insertUrl(baseUrl,fullUrl)

    def crawlSite(self,feed):
        c=urllib2.urlopen(feed)
        soup = BeautifulSoup(c, 'lxml')
        
        self.db.changeDate(feed)
        loweredfeed = feed.lower()
        '''
        Save the good URL's that are found
        '''
        for a in soup.findAll('a'):
            if a.has_attr('href'):
                ref = a['href']
                if ref.find('http') == 0:
                    self.saveUrl(Crawler.baseUrl,a['href'],loweredfeed)
                elif ref.find('/') == 0:
                    self.saveUrl(Crawler.baseUrl,self.baseUrl+ref,loweredfeed)
                    
        '''
        Tell a specific parser to parse the good URL's
        '''            
        if loweredfeed.find('cvenvacaturebank') > 0:
            if loweredfeed.find('/cv/') > 0 and loweredfeed.find('/koop/') < 0 and loweredfeed.find('/ideal/') < 0 and loweredfeed.find('.html') > 0:
                self.cvvp.parseCV(soup,feed)
            elif loweredfeed.find('/vacature/') > 0 and loweredfeed.find('.html') > 0 and loweredfeed.find('/reageer/') < 0 and loweredfeed.find('/doorsturen/') < 0:
                self.cvvp.parseVacature(soup,feed)
        elif loweredfeed.find('starapple') > 0:
            if loweredfeed.find('/kandidaat-') > 0 and loweredfeed.find('-download') < 0 and loweredfeed.find('/kandidaat-tell') < 0:
                self.sap.parseCV(soup,feed)
            elif loweredfeed.find('/vacature-') > 0:
                self.sap.parseVacature(soup,feed)
        elif loweredfeed.find('vacature.monsterboard') > 0:
            self.mbp.parseVacature(soup, feed)
                
    def startCrawler(self,base,amount=5):
        global baseUrl
        print "Crawling "+base
        Crawler.baseUrl = base
        feedList = self.db.gatherUrls(base.split('.')[1],amount)
        print "Crawler started for "+str(amount)+" crawls with a list of "+str(len(feedList))
        i = 1;
        
        '''
        See if there are URL's in the database with the feed as base.
        If not we start crawling it anew
        If there is we take these URL's and crawl them as if they are a new base URL
        '''
        if not feedList or len(feedList) == 0:
            try:
                self.crawlSite(base)
            except Exception,e:
                print "Could not crawl "+base
                print e
        else:
            for feed in feedList:
                try:
                    self.crawlSite(feed['fullurl'])
                except Exception,e:
                    print "Could not crawl "+feed['fullurl']
                    print e
                
                i+=1
                    
                '''
                Put a small delay in the crawling process in order not to flood the website with requests.
                Currently: 1.5 seconds
                Because: Developing and testing. Slower would slow down this proces.
                Plan: set to 10 seconds as a safe delay
                '''
                time.sleep(1.5)
                
                if i%50 == 0:
                    self.db.dbCommit()
                    
        self.db.dbCommit()
        print "Crawling "+base+" complete, remaining: "+str(amount-len(feedList))
        if len(feedList) < amount and len(feedList) != 0:
            print "Continue crawling with new list ..."
            self.startCrawler(base, amount-len(feedList))
        
        return "Crawling completed"