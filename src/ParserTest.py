import Crawler
import Parsers.SAParser as SAParser
import urllib2
from bs4 import BeautifulSoup
#import cherrypy #Let's make a webapp
#import flask

url = 'http://www.starapple.nl/kandidaat-2168-Medior_PHP_Developer/'

def start(self):
    c=urllib2.urlopen(url)
    soup = BeautifulSoup(c, 'lxml')
    SAParser.parseCV(soup,url)
    
start()