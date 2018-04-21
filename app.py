"""
Example python app with the Flask framework: http://flask.pocoo.org/
"""

from os import environ

from flask import Flask
from flask import render_template
#import jsonify
#from jsonify import *
from flask import *
import random
app = Flask(__name__)

from trans_db import *
from test_server import *

#  John Peurifoy 4/21
#   Note: This file has been modified for database tagging purposes
#  See swipe_and_get, remove if. 

myDb = TransDBConnector()
myDb.connect()

servercon = ServerConnector(myDb)

#Should pass the phoneName
@app.route('/api/login_method', methods = ['POST'])
def login_method():
    json = request.get_json()
    print("My json:", json)
    print("Logging user in and storing the phone data")
    #tempUser = json['username'].decode('ascii','ignore')
    tempUser = str(''.join([i if ord(i) < 128 else ' ' for i in json['username']]))
    #tempUser = unicode(json['username']).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    print(tempUser)
    servercon.login(tempUser)
    print("done logging in")

    #session['myNumber'] = random.randint(50,350)
    #print("myNUm:",session['myNumber'])

    pass
    return jsonify({'result':'true'})

#Pass phoneName
@app.route('/api/get_next_card', methods = ['POST'])
def get_next_card():
    json = request.get_json()

    #time.sleep(0.5)
    print("My json:", json)


    print("Getting next card.....")
    #tempUser = json['username'].encode('utf-8').strip()
    tempUser = str(''.join([i if ord(i) < 128 else ' ' for i in json['username']]))
    idToGet = int(servercon.getCardId(tempUser))
    print("IdToReturn is: " , idToGet)
    json = myDb.getNextCard(idToGet)
    json['id'] = idToGet
    #print("myNUm:",session['myNumber'])
    #session['myNumber'] = random.randint(50,350)
    #print("myNUm:",session['myNumber'])

    print("returning:")
    print(json)
    return jsonify({'card':json})

#Pass cardId,swipeChoice,and phoneName
@app.route('/api/swipe_card', methods = ['POST'])
def swipe_card():
    json = request.get_json()
    print("My json:", json)
    print("Swiping card....")
    #tempUser = json['username'].encode('utf-8').strip()
    tempUser = str(''.join([i if ord(i) < 128 else ' ' for i in json['username']]))
    servercon.swipeCard(int(json['cardId']),int(json['swipeChoice']),tempUser)


    print("Getting next card.....")
    #print("myNUm:",session['myNumber'])
    #session['myNumber'] = random.randint(50,350)
    #print("myNUm:",session['myNumber'])

    print("returning:")
    return jsonify({'success':True})

@app.route('/api/swipe_andGetID',methods=['POST'])
def swipe_and_get():
    json = request.get_json()

    tempUser = str(''.join([i if ord(i) < 128 else ' ' for i in json['username']]))
    idToGet = servercon.swipe_and_getID(int(json['cardId']),int(json['swipeChoice']),tempUser)

    json = myDb.getNextCard(idToGet)
    
    if True:
        idToGet = int(json['cardId'])+1.0
    json['id'] = idToGet

    print("returning:")
    print(json)
    return jsonify({'card':json})



@app.route('/api/get_message', methods = ['POST'])
def get_messages():
    json = request.get_json()
    print("My json:", json)

    print("Getting message.....")
    json = request.get_json()
    print("My json:", json)
    if json['user'] == "larry":
        return jsonify({'messages':'test1'})#['test1', 'test2']})
    return jsonify({'error':'no user found'})

@app.route('/')#, methods = ['GET'])
def index():
    print("Querying index....")
    #json = request.get_json()

    #if json['user'] == "larry":
    #    return jsonify({'messages':['test1', 'test2']})
    return jsonify({'message':'no user found'})

@app.route('/test')#, methods = ['GET'])
def index_2():
    print("Querying index....")
    #json = request.get_json()

    #if json['user'] == "larry":
    #    return jsonify({'messages':['test1', 'test2']})
    return jsonify({'message':'no user found'})

#@app.route('/')
#def index():
#    return render_template('index.html',
#                           powered_by=environ.get('POWERED_BY', 'Deis'))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = 5000#int(environ.get('PORT', 5000)

    app.debug = True
    app.secret_key = 'A0Zr98j/3yH!jmN]LWX/,?RT2390293023'

    app.run(host='0.0.0.0', port=port)
