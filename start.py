import bottle
from pymongo import MongoClient

app = application = bottle.Bottle() 

# mongodb connexion
client = MongoClient('localhost', 27017)
db = client.carb

@app.route('/')
def toto():
    #print(db.pdv.find())
    return "Test"

bottle.run(app, host='localhost', port=7001, reloader=True)
