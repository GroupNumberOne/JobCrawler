import psycopg2
import sys
import pprint
import urllib2
from bs4 import BeautifulSoup

conn_string = "host='localhost' dbname='postgres' user='postgres' password='GroeP1'"
conn = psycopg2.connect(conn_string)
    
def saveUrl(baseUrl,fullUrl):
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO urls
    (baseurl, fullurl)
    SELECT %s, %s
    WHERE
    NOT EXISTS (
    SELECT fullurl FROM urls WHERE fullurl = %s
    );""", (baseUrl,fullUrl,fullUrl)) 
 
c=urllib2.urlopen('http://www.jobbird.com/nl/vacatures/124/techniek-industrie')
soup = BeautifulSoup(c, "lxml")
baseUrl = 'http://www.jobbird.com'
for a in soup.findAll('a'):
    if a.has_attr('href'):
        ref = a['href']
        if(ref.find('http') == 0):
            saveUrl(baseUrl,a['href'])
        elif(ref.find('/') == 0):
            saveUrl(baseUrl,baseUrl+ref)

conn.commit()