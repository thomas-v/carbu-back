import bottle
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

app = application = bottle.Bottle() 

# mongodb connexion
client = MongoClient('localhost', 27017)
db = client.carb

@app.route('/stationsByDpt/<dpt>/<cp>')
def getStationsByDpt(dpt, cp):

    # get first stations from city
    city_stations = db.stations.find({'cp' : cp}, {'adresse' : 1, 'ville' : 1, 'cp' : 1, 'carburants' : 1, 'latitude' : 1, 'longitude' : 1,})

    # get stations by dpt 
    stations = db.stations.aggregate([{'$project' : {'adresse' : 1, 'ville' : 1, 'cp' : 1, 'carburants' : 1, 'latitude' : 1, 'longitude' : 1, 'dpt' : {'$substr' : ['$cp', 0, 2]}}}, {'$match' : { '$and' : [ {'dpt' : dpt}, {'cp' : {'$ne' : '78370'}} ] } }, { '$sort' : { 'cp' : 1 } }])

    city_stations_list = [({'adresse' : station['adresse'], 'ville' : station['ville'], 'cp' : station['cp'], 'latitude' : station['latitude'], 'longitude' : station['longitude'], 'carburants' : station['carburants']}) for station in city_stations]
    stations_list = city_stations_list + [({'adresse' : station['adresse'], 'ville' : station['ville'], 'cp' : station['cp'], 'latitude' : station['latitude'], 'longitude' : station['longitude'], 'carburants' : station['carburants']}) for station in stations]

    return json.dumps(stations_list)

@app.route('/stationsByPostCode/<postCode>')
def getStationsByPostCode(postCode):

    # get stations by postCode 
    station = db.stations.find_one({'cp' : postCode}, {'latitude' : 1, 'longitude' : 1, '_id' : 0});
    print(station)

    return json.dumps(station)

bottle.run(app, host='localhost', port=7001, reloader=True)
