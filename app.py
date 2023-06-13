from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'

ma = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

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
    venus = Planet(planet_name = 'Venus', planet_type = 'Class K', home_star = 'Sol', mass = 4.867e24, radius = 3760, distance = 67.24e6)
    earth = Planet(planet_name = 'Earth', planet_type = 'Class M', home_star = 'Sol', mass = 5.972e24, radius = 3959, distance = 92.96e6)

    save_record(mercury)
    save_record(venus)
    save_record(earth)

    test_user = User(first_name = 'William', last_name = 'Herschel', email = 'test@gmail.com', password = generate_password_hash('P@ssw0rd'))

    save_record(test_user)

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

def save_record(db_statement):
    db.session.add(db_statement)
    db.session.commit()
    print('Data saved successfully')

@app.route('/planets/list', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    result = planets_schema.dump(planets)
    
    return jsonify(data = result), 200

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    user = User(first_name = first_name, last_name = last_name, email = email, password = generate_password_hash(password))

    if check_if_user_exists(email):
        return jsonify(message = 'Email has already been taken.'), 409
    save_record(user)

    return jsonify(message = 'User created successfully'), 201

def check_if_user_exists(email):
    user = User.query.filter_by(email = email).first()
    return user

@app.route('/login', methods = ['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user_check = check_if_user_exists(email)

    if user_check and check_password_hash(user_check.password, password):
        access_token = create_access_token(identity=email)
        return jsonify(message='User logged in successfully', access_token=access_token), 200
    else:
        return jsonify(message='Incorrect email or password'), 401
    
# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)