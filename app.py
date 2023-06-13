from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created successfully')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database destroyed successfully')

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name = 'Mercury', planet_type = 'Class D', home_star = 'Sol', mass = 3.258e23, radius = 1516, distance = 35.98e6)
    mercury = Planet(planet_name = 'Mercury', planet_type = 'Class D', home_star = 'Sol', mass = 3.258e23, radius = 1516, distance = 35.98e6)
    mercury = Planet(planet_name = 'Mercury', planet_type = 'Class D', home_star = 'Sol', mass = 3.258e23, radius = 1516, distance = 35.98e6)

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
    
# database models
class User(db.model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

if __name__ == '__main__':
    app.run(debug=True)