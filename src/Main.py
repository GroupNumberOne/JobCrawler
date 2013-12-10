import Crawler
#import cherrypy #Let's make a webapp
#import flask

url = "http://www.cvenvacaturebank.nl"
def start():
    return Crawler.startCrawler(url,5)