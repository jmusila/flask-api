from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API'), 200

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify(message= 'Sorry, ' + name + ', you are not old enough'), 401
    else:
        return jsonify(message = 'Welcome ' + name + ', you are old enough'), 200
    
@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message= 'Sorry, ' + name + ', you are not old enough'), 401
    else:
        return jsonify(message = 'Welcome ' + name + ', you are old enough'), 200

if __name__ == '__main__':
    app.run(debug=True)