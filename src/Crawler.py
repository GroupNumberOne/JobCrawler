import psycopg2
import psycopg2.extras
import urllib2
from bs4 import BeautifulSoup
import time
import Parsers.CVenVParser as CVenVParser

try:
    conn_string = "host='145.24.222.158' dbname='INFPRJ01-56' user='postgres' password='GroeP1'"
    #conn_string = "host='localhost' dbname='postgres' user='postgres' password='GroeP1'"
    conn = psycopg2.connect(conn_string)
    print "Successfully connected to database"
except:
    print "Can't connect to the database"
    
db_name = "urls"
    
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
baseUrl = '';
    
def saveUrl(baseUrl,fullUrl):
    if fullUrl.lower().find('/cv/koop') > 0 or fullUrl.lower().find('/cv/ideal') > 0 or fullUrl.lower().find(baseUrl) > 0:
        return
    try:
        cursor.execute("""INSERT INTO """+db_name+"""
        (baseurl, fullurl)
        SELECT %s, %s
        WHERE
        NOT EXISTS (
        SELECT fullurl FROM urls WHERE fullurl = %s
        );""", (baseUrl,fullUrl,fullUrl))
    except:
        print "Could not insert "+fullUrl
 
def crawlSite(feed):
    print "Crawling "+feed+" ..."
    c=urllib2.urlopen(feed)
    soup = BeautifulSoup(c, "lxml")
    for a in soup.findAll('a'):
        if a.has_attr('href'):
            ref = a['href']
            if(ref.find('http') == 0):
                saveUrl(baseUrl,a['href'])
            elif(ref.find('/') == 0):
                saveUrl(baseUrl,baseUrl+ref)
    cursor.execute("""UPDATE """+db_name+""" SET lastcrawled = current_date WHERE fullUrl = '"""+feed+"""'""")
    if baseUrl.find('cvenvacaturebank') > 0 and feed.lower().find('/cv/') > 0 and feed.find('/koop/') < 0 and feed.find('/ideal/') < 0:
        CVenVParser.parseCV(soup)
            
def startCrawler(base,amount=20):
    print "Crawler started for "+str(amount)+" crawls"
    global baseUrl
    baseUrl = base
    cursor.execute("""SELECT * from """+db_name+""" WHERE baseurl LIKE '%"""+base+"""%' AND fullurl LIKE '%"""+base+"""%' AND (lastcrawled < current_date - integer '1' OR lastcrawled IS NULL)
    ORDER BY lastcrawled ASC NULLS FIRST LIMIT """+str(amount))
    feedList = cursor.fetchall()
    if not feedList:
        crawlSite(base)
    else:
        for feed in feedList:
            crawlSite(feed['fullurl'])
            time.sleep(1)
    
    #Select some urls from the database and crawl those sites. Finally, commit the changes.
    conn.commit()
    
    if len(feedList) < amount and len(feedList) != 0:
        startCrawler(base, amount-len(feedList))
    
#startCrawler("http://www.cvenvacaturebank.nl", 100)