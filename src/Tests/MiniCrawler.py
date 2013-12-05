import urllib2

class MiniCrawler():

    def printHeadlines(self, page):
        page = urllib2.urlopen(page)
        page = page.read()
        if (page.find("mw-headline") == -1):
            print "No headlines found"
            return
        
        headlineList = list()
        headlineStart = -1
        x=0
        
        while (page.find("mw-headline",headlineStart+1) != -1):
            headlineStart = page.find("mw-headline",headlineStart+1)
            start = page.find(">",headlineStart)
            end = page.find("<",start)
            headline = page[start+1:end]
            headlineList.append(headline)
            x = x + 1
            print headline
        
        for x in headlineList:
            print x
