"""
Example python app with the Flask framework: http://flask.pocoo.org/
"""

from os import environ

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/api/get_messages', methods = ['POST'])
def get_messages():
    json = request.get_json()
    if json['user'] == "larry":
        return jsonify({'messages':['test1', 'test2']})
    return jsonify({'error':'no user found'})

#@app.route('/')
#def index():
#    return render_template('index.html',
#                           powered_by=environ.get('POWERED_BY', 'Deis'))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = 8000#int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)