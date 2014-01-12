'''
JobCrawler Database Hanlder class
In charge of communication with the Database
'''

import psycopg2
import psycopg2.extras
import time
import traceback
import logging
import urllib2
import json

import SQL as sql

class DbHandler:    
    
    '''
    When this file is imported it will make a connection with the database
    
    Plan: - Make proper class with constructor
          - Have only 1 or 2 functions with all the SQL code to make more managable
    '''
    isConn = False    
    
    host = '145.24.222.158'
    dbname = 'INFPRJ01-56'
    user = 'prostgres'
    password = 'GroeP1'
    logging.basicConfig(filename='C:\log.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    
    db_urls = 'urls'
    db_cv = 'cv'
    db_vacature = 'vacatures'
    
    cvArray = {'voornaam':None,'achternaam':None,'tussenvoegsels':None,'opleiding':None,'jaren_werkervaring':None,'woonplaats':None,'cursussen':None,'it_kennis':None,'rijbewijs':None,'beroep':None}
    vacatureArray = {'it_kennis':None,'eisen':None,'plaats':None,'bedrijfsnaam':None,'functie':None,'uren':None,'salaris':None,'niveau':None,'omschrijving':None,'kennis':None,'dienstverband':None}


    x = 5 # max of 5 conn retries
    conn = None
    cursor = None
    
    def __init__(self):
        global conn,cursor,host,dbname,user,password
        while not DbHandler.isConn and self.x != 0:
            try:
                conn_string = 'host=145.24.222.158 dbname=INFPRJ01-56 user=postgres password=GroeP1'
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                DbHandler.isConn = True
            except:
                logging.info('Can\'t connect to the database')
                time.sleep(3)
                self.x= self.x- 1        
            
    def changeDate(self,feed,err=None):
        global cursor
        cursor.execute(sql.date_sql.format(self.db_urls),(err,feed))
        
    def gatherUrls(self,base,amount):
        global cursor
        if amount > 100:
            amount = 100
        cursor.execute(sql.gurl_sql.format(self.db_urls,base,base,str(amount)))
        return cursor.fetchall()
        
    def insertUrl(self,baseUrl,fullUrl):
        global cursor
        try:
            cursor.execute(sql.url_sql.format(self.db_urls),(baseUrl,fullUrl,fullUrl))
        except Exception,e:
            logging.debug('Could not insert url '+fullUrl)
            logging.debug(traceback.format_exc())
    
    def insertVacature(self,vacatureData,fullUrl):
        global cursor
        xArray = vacatureData
        vacatureData = self.vacatureArray
        for o in xArray:
            vacatureData[o] = xArray[o]
        vacatureData = self.formatInput(vacatureData)
        try:
            cursor.execute(sql.vacature_sql.format(self.db_vacature),(vacatureData['it_kennis'],vacatureData['eisen'],vacatureData['plaats'],vacatureData['bedrijfsnaam'],vacatureData['functie'],vacatureData['uren'],vacatureData['salaris'],vacatureData['niveau'],vacatureData['omschrijving'],vacatureData['kennis'],vacatureData['dienstverband'],fullUrl,vacatureData['it_kennis'],vacatureData['eisen'],vacatureData['plaats'],vacatureData['bedrijfsnaam'],vacatureData['functie'],vacatureData['uren'],vacatureData['salaris'],vacatureData['niveau'],vacatureData['omschrijving'],vacatureData['kennis'],vacatureData['dienstverband'],fullUrl,fullUrl))
        except Exception,e:
            logging.debug('Could not insert vacature '+fullUrl)
            logging.debug(traceback.format_exc())
            
        if vacatureData['plaats'] is not None:
            self.handleGeocode(vacatureData['plaats'])
        
    def insertCV(self,cvData,fullUrl):
        global cursor
        xArray = cvData
        cvData = self.cvArray
        for o in xArray:
            cvData[o] = xArray[o]
        cvData = self.formatInput(cvData)
        try:
            cursor.execute(sql.cv_sql.format(self.db_cv),(cvData['voornaam'],cvData['achternaam'],cvData['tussenvoegsels'],cvData['opleiding'],cvData['jaren_werkervaring'],cvData['woonplaats'],cvData['cursussen'],cvData['it_kennis'],cvData['rijbewijs'],cvData['beroep'],fullUrl,cvData['voornaam'],cvData['achternaam'],cvData['tussenvoegsels'],cvData['opleiding'],cvData['jaren_werkervaring'],cvData['woonplaats'],cvData['cursussen'],cvData['it_kennis'],cvData['rijbewijs'],cvData['beroep'],fullUrl,fullUrl))
        except Exception,e:
            logging.debug('Could not insert cv '+fullUrl)
            logging.debug(traceback.format_exc())
            
        if cvData['woonplaats'] is not None:
            self.handleGeocode(cvData['woonplaats'])
            
    def getCrawlstate(self,site):
        global cursor
        try:
            cursor.execute(sql.crawlstate_sql,(site,))
            #logging.info(cursor.fetchone()[0])
            return cursor.fetchone()
        except Exception,e:
            logging.debug("Could not get crawlstate")
            logging.debug(e)
            
    def getCrawlstateAll(self):
        global cursor
        try:
            cursor.execute(sql.crawlstate_all_sql)
            return cursor.fetchall()
        except Exception,e:
            logging.debug("Could not obtain crawl state")
            logging.debug(e)
            
    def changeCrawlStatus(self,status):
        global cursor,conn
        
        try:
            cursor.executemany(sql.crawlstate_change_single,([status['crawl_enabled'],0,'crawler'],[status['cv_enabled'],status['cv_amount'],'http://www.cvenvacaturebank.nl'],
                               [status['sa_enabled'],status['sa_amount'],'http://www.starapple.nl'],[status['mb_enabled'],status['mb_amount'],'http://www.monsterboard.nl']))
        except Exception,e:
            logging.debug(e)
            
    def changeCrawlStatusSingle(self,site,status):
        global cursor,conn
        
        try:
            cursor.execute(sql.crawlstate_change_single,(status,0,site))
        except Exception,e:
            logging.debug(e)
            
    def insertGeocode(self,city=None,lat=None,long=None):
        try:
            cursor.execute(sql.geocode_insert,(city,lat,long))
        except Exception,e:
            logging.debug(e)
            
    def checkGeocode(self,city):
        try:
            cursor.execute(sql.geocode_get,(city,))
            return cursor.fetchall()
        except Exception,e:
            logging.debug(e)
    
    def handleGeocode(self,city):
        try:
            if int(self.checkGeocode(city)[0][0]) == 0:
                url="http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % city.replace(' ','+')
                response = json.load(urllib2.urlopen(url))
                long = response['results'][0]['geometry']['location']['lng']
                lat = response['results'][0]['geometry']['location']['lat']
                self.insertGeocode(city,lat,long)
        except Exception,e:
            logging.debug(traceback.format_exc())
            
    def dbCommit(self):
        global conn
        conn.commit()
        
    def formatInput(self,input):
        for s in input:
            if isinstance(input[s],basestring):
                input[s] = input[s].lower().rstrip().lstrip()
        return input