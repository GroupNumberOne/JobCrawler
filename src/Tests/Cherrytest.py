import cherrypy
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import Main as Main
class HelloWorld(object):
    def index(self):
        #Main.start()
        return """<form action="startMain" method="post">
    <p><input type="submit" value="Start"/></p>
</form>"""
    index.exposed = True
    
    def startMain(self):
        return Main.start()
    startMain.exposed = True

cherrypy.quickstart(HelloWorld())