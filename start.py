import bottle
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

app = application = bottle.Bottle() 

# mongodb connexion
client = MongoClient('localhost', 27017)
db = client.carb

@app.route('/stations/<dpt>')
def getStationsByDpt(dpt):

    # get stations by postCode 
    stations = db.stations.aggregate([{'$project' : {'carburants' : 1, 'latitude' : 1, 'longitude' : 1, 'dpt' : {'$substr' : ['$cp', 0, 2]}}}, {'$match' : {'dpt' : dpt}}])
    
    stations_list = [({'latitude' : station['latitude'], 'longitude' : station['longitude'], 'carburants' : station['carburants']}) for station in stations]

    return json.dumps(stations_list)

bottle.run(app, host='localhost', port=7001, reloader=True)
