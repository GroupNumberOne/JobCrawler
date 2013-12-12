#import Crawler
import Parsers.SAParser as SAParser
import urllib2
from bs4 import BeautifulSoup
#import cherrypy #Let's make a webapp
#import flask

url = 'http://www.starapple.nl/vacature-43500-Als_kerstcadeau_starten_met_je_BI_development_baan_Ede_Gld/'
def start():
    c=urllib2.urlopen(url)
    soup = BeautifulSoup(c, 'lxml')
    SAParser.parseVacature(soup,url)