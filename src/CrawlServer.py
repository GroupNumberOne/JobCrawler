import cherrypy
from DbHandler import DbHandler
import os,inspect
from datetime import *

class Server():
    cherrypy.log.error_log.propagate = False
    cherrypy.log.access_log.propagate = False
    db = DbHandler()
    default_data = {'cv_enabled':False,'sa_enabled':False,'mb_enabled':False,'crawl_enabled':False,
                       'cv_amount':1000,'sa_amount':1000,'mb_amount':1000}
    def index(self):
        state = self.db.getCrawlstateAll()
        db_dump = {'cv_enabled':state[1][1],'sa_enabled':state[2][1],'mb_enabled':state[3][1],'crawl_enabled':state[0][1],
                       'cv_amount':state[1][2],'sa_amount':state[2][2],'mb_amount':state[3][2]}
        return self.form(db_dump)
    index.exposed = True
    
    def form(self,status=None):
        if status is None:
            status = self.default_data
        
        if status['cv_enabled']:
            cv_checked = 'checked'
        else:
            cv_checked = ''
            
        if status['sa_enabled']:
            sa_checked = 'checked'
        else:
            sa_checked = ''
            
        if status['mb_enabled']:
            mb_checked = 'checked'
        else:
            mb_checked = ''
            
        if status['crawl_enabled']:
            crawl_checked = 'checked'
        else:
            crawl_checked = ''
        
        return """<form action="changestatus" method="post">
        <table border=0>
            <tr>
                <th>Website</th>
                <th>Enabled</th>
                <th>Amount of crawls</th>
            </tr>
            <tr>
                <td>http://www.cvenvacaturebank.nl</td>
                <td><input type="checkbox" name="cv_on" {0} value="True"/></td>
                <td><input type="text" name="cv_amount" value="{4}"/></td>
            </tr>
            <tr>
                <td>http://www.starapple.nl</td>
                <td><input type="checkbox" name="sa_on" {1} value="True"/></td>
                <td><input type="text" name="sa_amount" value="{5}"/></td>
            </tr>
            <tr>
                <td>http://www.monsterboard.nl</td>
                <td><input type="checkbox" name="mb_on" {2} value="True"/></td>
                <td><input type="text" name="mb_amount" value="{6}"/></td>
            </tr>
            <tr>
                <td>Crawler</td>
                <td><input type="checkbox" name="crawl_on" {3} value="True"/></td>
                <td></td>
            </tr>
        </table>
        <input type="submit" value="Change"/>
        </form>""".format(cv_checked,sa_checked,mb_checked,crawl_checked,status['cv_amount'],status['sa_amount'],status['mb_amount'])
    #addition.exposed = True
    
    def changestatus(self,cv_on=False,cv_amount=1000,sa_amount=1000, mb_amount=1000,sa_on=False,crawl_on=True,mb_on=False):
        curr_status = {'cv_enabled':cv_on == "True",'sa_enabled':sa_on == "True",'mb_enabled':mb_on == "True",'crawl_enabled':crawl_on == "True",
                       'cv_amount':int(cv_amount),'sa_amount':int(sa_amount),'mb_amount':int(mb_amount)}
        self.db.changeCrawlStatus(curr_status)
        self.db.dbCommit()
        return self.form(curr_status)
    changestatus.exposed = True
    
    def dashboard(self,name=None):
        if name == "bob":
            return self.dashboardBob()
        else:
            return "No dashboard selected"
    dashboard.exposed = True
    
    def dashboardBob(self):
        dates = []
        numbers = []
        crawldata = self.db.getCrawlData(7)
        check_date = date.today()-timedelta(days=6)
        checked = 0
        while checked < 7:
            found = False
            for i in crawldata:
                if i[0] == check_date:
                    dates.append(i[0].strftime("%d-%m-%Y"))
                    numbers.append(str(int(i[1])))
                    found = True
            if not found:
                dates.append(check_date.strftime("%d-%m-%Y"))
                numbers.append("0")
            checked += 1
            check_date += timedelta(days=1)
            
        datestring = "['" + "','".join(dates) + "']"
        numberstring = "[" + ",".join(numbers) + "]"
        
        #return numberstring
        
        return """  <head>
                        <title>Dashboard van Bob</title>
                        <script src="/static/Chart.js"></script>
                    </head>
                    <body>
                    <canvas id="statChart" width="400" height="400"></canvas>
                    <script>
                        var ctx = document.getElementById("statChart").getContext("2d");
                        var data = {
                            labels : %s,
                            datasets : [
                                {
                                    fillColor : "rgba(151,187,205,0.5)",
                                    strokeColor : "rgba(151,187,205,1)",
                                    pointColor : "rgba(151,187,205,1)",
                                    pointStrokeColor : "rgba(151,187,205,0)",
                                    data : %s
                                }
                            ]
                        }
                        var myNewChart = new Chart(ctx).Line(data);
                    </script>
                    </body>""" % (datestring,numberstring)
    
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
config = {'global':
                {'tools.staticdir.root':path,
                 'server.socket_port': 8081, 
                 'server.socket_host':'0.0.0.0'
                },
          '/static':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': 'static',
                }
        }
cherrypy.quickstart(Server(),config=config)