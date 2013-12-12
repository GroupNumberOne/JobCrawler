'''
JobCrawler Database Hanlder class
In charge of communication with the Database
'''

import psycopg2
import psycopg2.extras

'''
When this file is imported it will make a connection with the database

Plan: - Make proper class with constructor
      - Make sure class is instantiated when the crawler starts and connection closed when crawler stops.
      - Use hard-coded strings for conn
      - Have only 1 or 2 functions with all the SQL code to make more managable
'''
try:
    conn_string = "host='145.24.222.158' dbname='INFPRJ01-56' user='postgres' password='GroeP1'"
    conn = psycopg2.connect(conn_string)
    print "Successfully connected to database"
except:
    print "Can't connect to the database"
    
db_urls = "urls"
db_cv = "cv"
db_vacature = "vacatures"
    
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def insertVacature(vacatureData,fullUrl):
    try:
        cursor.execute(""" UPDATE """+db_vacature+""" SET functie=%s, niveau=%s, dienstverband=%s, plaats=%s, kennis=%s, omschrijving=%s WHERE url=%s;
        INSERT INTO """+db_vacature+"""
        (functie, niveau, dienstverband, plaats, kennis, omschrijving, url)
        SELECT %s, %s, %s, %s, %s, %s, %s
        WHERE
        NOT EXISTS (
        SELECT url FROM """+db_vacature+""" WHERE url = %s
        );""", (vacatureData['beroep'],vacatureData['opleiding'],vacatureData['dienstverband'],vacatureData['plaats'],vacatureData['kennis'],vacatureData['omschrijving'],fullUrl,vacatureData['beroep'],vacatureData['opleiding'],vacatureData['dienstverband'],vacatureData['plaats'],vacatureData['kennis'],vacatureData['omschrijving'],fullUrl,fullUrl))
    except Exception,e:
        print "Could not insert "+fullUrl
        print str(e)
        print vacatureData
    
def insertCV(cvData,fullUrl):
    try:
        cursor.execute(""" UPDATE """+db_cv+""" SET opleiding=%s, woonplaats=%s, rijbewijs=%s, beroep=%s WHERE url=%s;
        INSERT INTO """+db_cv+"""
        (opleiding, woonplaats, rijbewijs, beroep, url)
        SELECT %s, %s, %s, %s, %s
        WHERE
        NOT EXISTS (
        SELECT url FROM """+db_cv+""" WHERE url = %s
        );""", (cvData['opleiding'],cvData['woonplaats'],cvData['rijbewijs'],cvData['beroep'],fullUrl,cvData['opleiding'],cvData['woonplaats'],cvData['rijbewijs'],cvData['beroep'],fullUrl,fullUrl))
    except Exception,e:
        print "Could not insert "+fullUrl
        print str(e)
        print cvData
    
def insertUrl(baseUrl,fullUrl):
    try:
        cursor.execute("""INSERT INTO """+db_urls+"""
        (baseurl, fullurl)
        SELECT %s, %s
        WHERE
        NOT EXISTS (
        SELECT fullurl FROM urls WHERE fullurl = %s
        );""", (baseUrl,fullUrl,fullUrl))
    except Exception,e:
        print "Could not insert "+fullUrl
        print str(e)
        
def changeDate(feed):
    cursor.execute("""UPDATE """+db_urls+""" SET lastcrawled = current_date WHERE fullUrl = '"""+feed+"""'""")
    
def gatherUrls(base,amount):
    cursor.execute("""SELECT * from """+db_urls+""" WHERE baseurl LIKE '%"""+base+"""%' AND fullurl LIKE '%"""+base+"""%' AND (lastcrawled <= current_date - integer '2' OR lastcrawled IS NULL)
    ORDER BY lastcrawled ASC NULLS FIRST LIMIT """+str(amount))
    return cursor.fetchall()
        
def dbCommit():
    conn.commit()