from flask import Flask, request, jsonify, make_response,  redirect, url_for, render_template

from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired

import os, requests, hashlib

app = Flask(__name__)

SECRET_KEY = os.urandom(32).hex()
app.config['SECRET_KEY'] = SECRET_KEY

tokens = {}

class PasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired()])

def passwordHash(password: str, salt=None):
    salt = salt or os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,10000)
    return (salt+key)

@app.route('/reset/<string:token>', methods=["GET", "POST"])
def resetWithToken(token):
    usr = None
    try: 
        usr = tokens[token]
    except:
        return make_response('Invalid address',404)

    form = PasswordForm()

    if form.validate_on_submit():
        r = requests.patch('http://127.0.0.1:5000/api/users', json=({'password':passwordHash(form.password.data).hex()}), params={'username':usr})
        tokens.pop(token)

        return make_response('Password succesfully changed',200)
    
    return render_template('form.html', form=form, token=token)

@app.route('/token/<string:user>',methods=["POST"])
def addUserToReset(user):
    if user != None:
        r = os.urandom(32).hex()
        tokens[r] = user
        return make_response(jsonify({'token': r}),201)
    return make_response('Invalid data', 400)

@app.route('/token',methods=['GET'])
def tokenList():
    try: 
        key = request.args['key']
        if key == SECRET_KEY:
            return make_response(tokens,200)
    except Exception as _:  
        pass
    
    return make_response('Invalid address',404)
    

if __name__ == '__main__':
    print(SECRET_KEY)
    app.run(debug=True,host='0.0.0.0',port='5050', ssl_context='adhoc')