import psycopg2
import psycopg2.extras
import urllib2
from bs4 import BeautifulSoup

try:
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='GroeP1'"
except:
    print "Can't connect to the database"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
baseUrl = '';
    
def saveUrl(baseUrl,fullUrl):
    try:
        cursor.execute("""INSERT INTO urls
        (baseurl, fullurl)
        SELECT %s, %s
        WHERE
        NOT EXISTS (
        SELECT fullurl FROM urls WHERE fullurl = %s
        );""", (baseUrl,fullUrl,fullUrl))
        print "Inserted "+fullUrl
    except:
        print "Could not insert "+fullUrl
 
def crawlSite(feed):
    print "Crawling "+feed+"..."
    c=urllib2.urlopen(feed)
    soup = BeautifulSoup(c, "lxml")
    for a in soup.findAll('a'):
        if a.has_attr('href'):
            ref = a['href']
            if(ref.find('http') == 0):
                saveUrl(baseUrl,a['href'])
            elif(ref.find('/') == 0):
                saveUrl(baseUrl,baseUrl+ref)
            
def startCrawler(base,amount=20):
    global baseUrl
    baseUrl = base
    cursor.execute("""SELECT * from urls WHERE baseUrl LIKE '%"""+base+"""%' LIMIT """+str(amount))
    feedList = cursor.fetchall()
    print feedList
    if not feedList:
        crawlSite(base)
    else:
        for feed in feedList:
            crawlSite(feed['fullurl'])
    
    #Select some urls from the database and crawl those sites. Finally, commit the changes.
    conn.commit()
    
startCrawler("http://www.cvenvacaturebank.nl")