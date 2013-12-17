'''
JobCrawler Database Hanlder class
In charge of communication with the Database
'''

import psycopg2
import psycopg2.extras
import time

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
     
    db_urls = 'urls'
    db_cv = 'cv'
    db_vacature = 'vacatures'
    
    cvArray = {'voornaam':None,'achternaam':None,'tussenvoegsels':None,'opleiding':None,'jaren_werkervaring':None,'woonplaats':None,'cursussen':None,'it_kennis':None,'rijbewijs':None,'beroep':None}
    vacatureArray = {'it_kennis':None,'eisen':None,'plaats':None,'bedrijfsnaam':None,'functie':None,'uren':None,'salaris':None,'niveau':None,'omschrijving':None,'kennis':None,'dienstverband':None}


    x = 5 # max of 5 conn retries
    conn = None    
    
    def __init__(self):
        while not self.isConn and self.x != 0:
            try:
                conn_string = 'host=%s dbname=%s user=%s password=%s' % self.host,self.dbname,self.user,self.password
                self.conn = psycopg2.connect(conn_string)
                print 'Successfully connected to database'
                self.isConn = True
            except:
                print 'Can\'t connect to the database'
                time.sleep(5)
                self.x= self.x- 1
            
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
    def changeDate(self,feed):
        self.cursor.execute(sql.date_sql % self.db_urls,feed)
        
    def gatherUrls(self,base,amount):
        self.cursor.execute(sql.gurl_sql % self.db_urls,base,base,str(amount))
        return self.cursor.fetchall()
        
    def insertUrl(self,baseUrl,fullUrl):
        try:
            self.cursor.execute(sql.url_sql % self.db_urls,baseUrl,fullUrl,fullUrl)
        except Exception,e:
            print 'Could not insert '+fullUrl
            print str(e)
    
    def insertVacature(self,vacatureData,fullUrl):
        xArray = vacatureData
        vacatureData = self.vacatureArray
        for o in xArray:
            vacatureData[o] = xArray[o]
        try:
            self.cursor.execute(sql.vacature_sql % self.db_vacature,vacatureData['it_kennis'],vacatureData['eisen'],vacatureData['plaats'],vacatureData['bedrijfsnaam'],vacatureData['functie'],vacatureData['uren'],vacatureData['salaris'],vacatureData['niveau'],vacatureData['omschrijving'],vacatureData['kennis'],vacatureData['dienstverband'],fullUrl,self.db_vacature,vacatureData['it_kennis'],vacatureData['eisen'],vacatureData['plaats'],vacatureData['bedrijfsnaam'],vacatureData['functie'],vacatureData['uren'],vacatureData['salaris'],vacatureData['niveau'],vacatureData['omschrijving'],vacatureData['kennis'],vacatureData['dienstverband'],fullUrl,self.db_vacature,fullUrl)
        except Exception,e:
            print 'Could not insert '+fullUrl
            print str(e)
        
    def insertCV(self,cvData,fullUrl):
        xArray = cvData
        cvData = self.cvArray
        for o in xArray:
            cvData[o] = xArray[o]
        try:
            self.cursor.execute(sql.cv_sql % self.db_cv,cvData['voornaam'],cvData['achternaam'],cvData['tussenvoegsels'],cvData['opleiding'],cvData['jaren_werkervaring'],cvData['woonplaats'],cvData['cursussen'],cvData['it_kennis'],cvData['rijbewijs'],cvData['beroep'],fullUrl,self.db_cv,cvData['voornaam'],cvData['achternaam'],cvData['tussenvoegsels'],cvData['opleiding'],cvData['jaren_werkervaring'],cvData['woonplaats'],cvData['cursussen'],cvData['it_kennis'],cvData['rijbewijs'],cvData['beroep'],fullUrl,self.db_cv,fullUrl)
        except Exception,e:
            print 'Could not insert '+fullUrl
            print str(e)
            
    def dbCommit(self):
        self.conn.commit()