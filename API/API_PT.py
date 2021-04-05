from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from sqlalchemy.orm import validates
from marshmallow import fields, validate

app = Flask(__name__) 
api = Api(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ptDatabase.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app) 
ma = Marshmallow(app)

####### User ##############

class User(db.Model): 
    user  = db.Table('user', 
    db.Column('id', db.Integer, primary_key=True),
    db.Column('username', db.String(11), unique=True),
    db.Column('password', db.String(32)))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

user_schema = UserSchema() 
users_schema = UserSchema(many=True)

class UserManager(Resource):
    
    @staticmethod
    def get():
        try: username = request.args['username']
        except Exception as _: username = None

        if not username:
            users = User.query.all()
            return make_response(jsonify(users_schema.dump(users)), 200)
        else:
            user = User.query.filter_by(username = username).first()
            return make_response(jsonify(user_schema.dump(user)), 200)

    @staticmethod
    def post():
        username = request.json['username']
        password = request.json['password']

        if username != None and password != None and User.query.filter_by(username = username).first() == None:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({'Message': f'User {username} inserted.'}), 201)
       
    @staticmethod
    def put():
        try: username = request.args['username']
        except Exception as _: username = None

        if not username:
            return make_response(jsonify({ 'Message': 'Must provide the proper username' }), 400)

        user = User.query.filter_by(username = username).first()

        if user == None:
            return make_response(jsonify({ 'Message': 'User not exist!' }), 404)

        username_new = request.json['username']
        password_new = request.json['password']
        user.password = password_new
        user.username = username_new

        db.session.commit()
        return make_response(jsonify({'Message': f'User {user.username} altered.'}), 200)

    @staticmethod
    def patch():
        try: username = request.args['username']
        except Exception as _: username = None

        if not username:
            return make_response(jsonify({ 'Message': 'Must provide the proper username' }), 400)

        user = User.query.filter_by(username = username).first()

        if user == None:
            return make_response(jsonify({ 'Message': 'User not exist!' }), 404)

        username_new = request.json['username']
        password_new = request.json['password']

        if username_new != None:
            user.username = username_new

        if password_new != None:
            user.password = password_new 

        db.session.commit()
        return make_response(jsonify({'Message': f'User {user.username} altered.'}), 200)

    @staticmethod
    def delete():
        try: username = request.args['username']
        except Exception as _: username = None

        if not username:
            return make_response(jsonify({ 'Message': 'Must provide the user username' }), 400)

        user = User.query.get(username)

        if user == None:
            return make_response(jsonify({ 'Message': 'User not exist!' }), 404)

        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({'Message': f'User {username} deleted.'}), 200)


api.add_resource(UserManager, '/api/users')

####### History ##############

class History(db.Model): 
    history  = db.Table('history', 
    db.Column('id', db.Integer, primary_key=True),
    db.Column('first_username', db.String(32), db.ForeignKey('user.username')),
    db.Column('second_username', db.String(32), db.ForeignKey('user.username')))

    def __init__(self, first_username, second_username):
        self.first_username = first_username
        self.second_username = second_username

class HistorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_username', 'second_username')

history_schema = HistorySchema() 
histories_schema = HistorySchema(many=True)

class HistoryManager(Resource):
    
   

api.add_resource(HistoryManager, '/api/history')

####### History Content ##############

class HistoryContent(db.Model): 
    historyContent  = db.Table('historyContent', 
    db.Column('id', db.Integer, db.ForeignKey('history.id'), primary_key=True),
    db.Column('content', db.Text))

    def __init__(self, content):
        self.content = content
        self.second_username = second_username

class HistoryContentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content')

historyContent_schema = HistoryContentSchema() 
historiesContent_schema = HistoryContentSchema(many=True)

class HistoryContentManager(Resource):
    
   

api.add_resource(HistoryContentManager, '/api/history-content')