from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from sqlalchemy.orm import validates, Session
from marshmallow import fields, validate
from datetime import datetime


app = Flask(__name__) 
api = Api(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ptDatabase.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app) 
ma = Marshmallow(app)

####### User ##############

class User(db.Model): 
    user  = db.Table('user', 
    db.Column('id', db.Integer, primary_key=True),
    db.Column('username', db.String(64), unique=True),
    db.Column('email', db.String(320)),
    db.Column('password', db.String(128)))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

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
        email = request.json['email']
        password = request.json['password']

        if (email and username and password) != None and User.query.filter_by(username = username).first() == None:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({'Message': f'User {username} inserted.'}), 201)
        elif User.query.filter_by(username = username).first() != None:
            return make_response(jsonify({'Message': f'User {username} exist.'}), 409)
        else:
            return make_response(jsonify({'Message': 'BAD_REQUEST'}), 400)
            
       
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
        email_new = request.json['email']
        password_new = request.json['password']
        user.password = password_new
        user.username = username_new
        user.email = email_new

        db.session.commit()
        return make_response(jsonify({'Message': f'User {user.username} altered.'}), 200)

    @staticmethod
    def patch():
        try: 
            username = request.args['username']
        except Exception as _: 
            username = None
            
        try:
            username_new = request.json['username']
        except Exception as _:
            username_new = None

        try:
            password_new = request.json['password']
        except Exception as _:
            password_new = None
        
        try:
            email_new = request.json['password']
        except Exception as _:
            email_new = None

        if username == None:
            return make_response(jsonify({ 'Message': 'Must provide the proper username' }), 400)

        user = User.query.filter_by(username = username).first()

        if user == None:
            return make_response(jsonify({ 'Message': 'User not exist!' }), 404)

        if username_new != None:
            user.username = username_new

        if password_new != None:
            user.password = password_new 
        
        if email_new != None:
            user.email = email_new

        db.session.commit()
        return make_response(jsonify({'Message': f'User {user.username} altered.'}), 200)

    @staticmethod
    def delete():
        try: username = request.args['username']
        except Exception as _: username = None

        if not username:
            return make_response(jsonify({ 'Message': 'Must provide the user username' }), 400)

        user = User.query.filter_by(username = username).first()

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
    db.Column('first_username', db.String(64), db.ForeignKey('user.username')),
    db.Column('second_username', db.String(64), db.ForeignKey('user.username')))
    histories = db.relationship('HistoryContent', backref='history', lazy=True)

    def __init__(self, first_username, second_username):
        self.first_username = first_username
        self.second_username = second_username

class HistorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_username', 'second_username')

history_schema = HistorySchema() 
histories_schema = HistorySchema(many=True)

####### History Content ##############

class HistoryContent(db.Model): 
    history  = db.Table('history_content',
    db.Column('id', db.Integer, primary_key=True), 
    db.Column('history_id', db.Integer, db.ForeignKey('history.id')),
    db.Column('username', db.String(64), db.ForeignKey('user.username')),
    db.Column('content', db.Text),
    db.Column('date', db.DateTime, nullable=False, default=datetime.utcnow))

    def __init__(self, history_id, username, content):
        self.history_id = history_id
        self.username = username
        self.content = content

class HistoryContentSchema(ma.Schema):
    class Meta:
        fields = ('history_id', 'username', 'content', 'date')

historyContent_schema = HistoryContentSchema() 
historiesContent_schema = HistoryContentSchema(many=True)

####### General History Manager ##############

class HistoryManager(Resource):
    
    @staticmethod
    def get():
        try: 
            first_username = request.args['first_username']
            second_username = request.args['second_username']
        except Exception as _: 
            first_username = None
            second_username = None
        
        if (first_username and second_username) == None:
            content = HistoryContent.query.all()
            return make_response(jsonify(historiesContent_schema.dump(content)), 200)
        else:
            try: history_id = History.query.filter_by(first_username = first_username, second_username = second_username).first().id
            except Exception as _: history_id = None
            if history_id == None:
                history_id = History.query.filter_by(first_username = second_username, second_username = first_username).first().id
            if history_id == None:
                return make_response(jsonify({'Message': 'NOT_EXIST'}), 404)
            else:
                historyContent = HistoryContent.query.filter_by(history_id = history_id).all()
                return make_response(jsonify(historiesContent_schema.dump(historyContent)), 200)
    
    @staticmethod
    @app.route("/api/history-manager/historyID")
    def getHistoryId():
        try: 
            first_username = request.args['first_username']
            second_username = request.args['second_username']
        except Exception as _: 
            first_username = None
            second_username = None
        
        if (first_username and second_username) != None:
            try: history_id = History.query.filter_by(first_username = first_username, second_username = second_username).first().id
            except Exception as _: history_id = None
            if history_id == None:
                try: history_id = History.query.filter_by(first_username = second_username, second_username = first_username).first().id
                except Exception as _: history_id = None
            if history_id == None:
                return make_response(jsonify({'Message': 'NOT_EXIST'}), 404)
            else:
                return make_response(jsonify({"history_id" : history_id}), 200)

    @staticmethod
    def post():
        try:
            history_id = request.json['history_id']
            username = request.json['username']
            content = request.json['content']
        except Exception as _:
            history_id = None
            username = None
            content = None
        
        try:
            first_username = request.json['first_username']
            second_username = request.json['second_username']
        except Exception as _:
            first_username = None
            second_username = None
        
        if (history_id and username and content) != None:
            if (History.query.filter_by(id = history_id).first() and User.query.filter_by(username = username).first()) != None:
                historyContent = HistoryContent(history_id, username, content)
                db.session.add(historyContent)
                db.session.commit()
                return make_response(jsonify({'Message': 'CREATED'}), 201)
            else:
                return make_response(jsonify({'Message': 'BAD_REQUEST'}), 400)
        
        if (first_username and second_username) != None:
            if (History.query.filter_by(
                first_username = first_username, second_username = second_username).first() and
                History.query.filter_by(
                first_username = second_username, second_username = first_username).first()) == None:
                
                history = History(first_username, second_username)
                db.session.add(history)
                db.session.commit()
                return make_response(jsonify({'Message': 'CREATED'}), 201)
            else:
                return make_response(jsonify({'Message': 'CONFLICT'}), 409)
        
    @staticmethod
    def delete():
        try: 
            first_username = request.args['first_username']
            second_username = request.args['second_username']
        except Exception as _: 
            first_username = None
            second_username = None

        if not first_username or second_username:
            return make_response(jsonify({ 'Message': 'Must provide proper args.' }), 400)

        history = History.query.get(first_username = first_username, second_username = second_username)
        history_content = HistoryContent.query.filter_by(id = history.id).all()
        
        if (history or history_content) == None:
            return make_response(jsonify({ 'Message': 'History not exist!' }), 404)

        db.session.delete(history)
        db.session.delete(history_content)
        db.session.commit()

        return make_response(jsonify({'Message': f'History {id} deleted.'}), 200)

api.add_resource(HistoryManager, '/api/history-manager')  

if __name__ == '__main__':
    app.run(debug=True)