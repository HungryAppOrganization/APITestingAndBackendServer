"""
Example python app with the Flask framework: http://flask.pocoo.org/
"""

from os import environ

from flask import Flask
from flask import render_template

app = Flask(__name__)

"""
Example python app with the Flask framework: http://flask.pocoo.org/
"""

from os import environ

from flask import Flask
from flask import render_template
#import jsonify
#from jsonify import *
from flask import *
app = Flask(__name__)

@app.route('/api/get_message', methods = ['POST'])
def get_messages():
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
    port = 5000#int(environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)