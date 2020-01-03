import bottle
from pymongo import MongoClient
from datetime import datetime
import json

app = application = bottle.Bottle() 

# mongodb connexion
client = MongoClient('localhost', 27017)
db = client.carb

@app.route('/stations/<cp>')
def getStationsByPostCode(cp):
    
    # current date
    today = datetime.today().strftime('%Y-%m-%d')

    # get stations by postCode 
    stations = db.pdv.find({'cp' : cp}, {'latitude' : 1, 'longitude' : 1, today : 1})
    stations_list = [({'latitude' : station['latitude'], 'longitude' : station['longitude'], 'carburants' : station[today]}) for station in stations]

    return json.dumps(stations_list)

bottle.run(app, host='localhost', port=7001, reloader=True)
