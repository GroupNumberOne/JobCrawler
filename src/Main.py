import Crawler
import cherrypy #Let's make a webapp
import flask

url = "http://www.cvenvacaturebank.nl"

Crawler.startCrawler(url,10000)