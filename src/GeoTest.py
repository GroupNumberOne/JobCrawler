from DbHandler import DbHandler

db = DbHandler()

db.handleGeocode('groningen')
db.dbCommit()