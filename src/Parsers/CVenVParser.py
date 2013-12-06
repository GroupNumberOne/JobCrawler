import psycopg2
from bs4 import BeautifulSoup
import re

try:
    #conn_string = "host='145.24.222.158' dbname='INFPRJ01-56' user='postgres' password='GroeP1'"
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='GroeP1'"
    conn = psycopg2.connect(conn_string)
except:
    print "Can't connect to the database"

def parseCV(soup):
    print "Parsing cv ..."
    cvData = []
    if ''.join(soup.findAll(text=True)).find("Beroep") > 0: #Means we have someone with ICT experience
        beroep = soup.find('span',text=re.compile('.*Beroep.*')).parent.find('div').text
        opleiding = soup.find('span',text=re.compile('.*Niveau.*')).parent.find('div').text
        woonplaats = soup.find('span',text=re.compile('.*Woonplaats.*')).parent.find('div').text
        geslacht = soup.find('span',text=re.compile('.*Geslacht.*')).parent.find('div').text
        provincie = soup.find('span',text=re.compile('.*Provincie.*')).parent.find('div').text
        leeftijd = soup.find('span',text=re.compile('.*Leeftijd.*')).parent.find('div').text.split()[0]
        
        cvData = {'beroep':beroep, 'opleiding': opleiding, 'woonplaats':woonplaats,'geslacht':geslacht,'provincie':provincie,'leeftijd':leeftijd}
        print cvData
        print cvData['beroep']
        