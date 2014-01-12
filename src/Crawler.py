# -*- coding: utf-8 -*-
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
import logging
import traceback


class Crawler:    
    
    baseURL = ''
    logging.basicConfig(filename='C:\log.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    sap = SAParser()
    cvvp = CVenVParser()
    mbp = MBParser()
    db = DbHandler()
    crawltries = 0
    
    '''
    If the current URL is a website of interest (containing useful information)
    we store it in the database
    '''    
    def saveUrl(self,baseUrl,fullUrl,loweredfeed):
        if loweredfeed.find('cvenvacaturebank') > 0:
            if fullUrl.lower().find('/cv/koop') > 0 or fullUrl.lower().find('/cv/ideal') > 0 or fullUrl.lower().find('/vacature/doorsturen') > 0 or fullUrl.lower().find('vacature/reageer') > 0:
                return

        self.db.insertUrl(baseUrl,fullUrl)

    def crawlSite(self,feed):
        #if not isinstance(feed,unicode):
            #feed = unicode(feed,'UTF-8')
            #print isinstance(feed,unicode)
        
        c=urllib2.urlopen(feed)
        soup = BeautifulSoup(c, 'html5lib')
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
        if loweredfeed.find('cvenvacaturebank') >= 0:
            if loweredfeed.find('/cv/') > 0 and loweredfeed.find('/koop/') < 0 and loweredfeed.find('/ideal/') < 0 and loweredfeed.find('.html') > 0:
                self.cvvp.parseCV(soup,feed)
            elif loweredfeed.find('/vacature/') >= 0 and loweredfeed.find('.html') > 0 and loweredfeed.find('/reageer/') < 0 and loweredfeed.find('/doorsturen/') < 0:
                self.cvvp.parseVacature(soup,feed)
        elif loweredfeed.find('starapple') > 0:
            if loweredfeed.find('/profielen/') >= 0 and (loweredfeed.find('/profielen/')+11)<len(loweredfeed):
                self.sap.parseCV(soup,feed)
            elif loweredfeed.find('/vacatures/') >= 0 and (loweredfeed.find('/vacatures/')+11)<len(loweredfeed):
                self.sap.parseVacature(soup,feed)
        elif loweredfeed.find('vacature.monsterboard') >= 0 and loweredfeed.find('.aspx') >= 0:
            self.mbp.parseVacature(soup, feed)
                
    def startCrawler(self,base,amount=1):
        global baseUrl,crawltries
        Crawler.baseUrl = base
        feedList = self.db.gatherUrls(base.split('.')[1],amount)
        logging.info("Crawling {0}. Remaining crawls this run: {1}".format(base,amount))
        i = 1;
        
        '''
        See if there are URL's in the database with the feed as base.
        If not we start crawling it anew
        If there is we take these URL's and crawl them as if they are a new base URL
        '''
        if not feedList or len(feedList) == 0:
            try:
                self.crawlSite(base)
                Crawler.crawltries += 1
            except Exception,e:
                logging.debug("Could not crawl "+base)
                logging.debug(e)
        else:
            Crawler.crawltries = 0
            for feed in feedList:
                try:
                    self.crawlSite(feed['fullurl'])
                except urllib2.HTTPError,e:
                    self.db.changeDate(feed['fullurl'],e.code)
                except Exception,e:
                    logging.debug("Could not crawl "+feed['fullurl'])
                    logging.debug(traceback.format_exc())
                    self.db.changeDate(feed['fullurl'])
                
                i+=1
                    
                '''
                Put a small delay in the crawling process in order not to flood the website with requests.
                Currently: 1.5 seconds
                Because: Developing and testing. Slower would slow down this proces.
                Plan: set to 10 seconds as a safe delay
                '''
                time.sleep(10)
                
                if i%50 == 0:
                    self.db.dbCommit()
           
        self.db.dbCommit()
        if Crawler.crawltries >=2:
            self.db.changeCrawlStatusSingle(base, False)
        elif len(feedList) < amount and len(feedList) != 0:
            self.startCrawler(base, amount-len(feedList))