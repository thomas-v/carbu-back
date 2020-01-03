import bottle
import pymongo

app = application = bottle.Bottle() 

@app.route('/')
def toto():
    return "Test"

bottle.run(app, host='localhost', port=7001, reloader=True)
