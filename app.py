from flask import (Flask, session, request)
import pymongo
from os import environ
from functools import wraps
from flask import redirect

app = Flask(__name__)
app.secret_key = 'my_secret_key'

MONGO_PASS = environ.get('MONGO_PASS')
mongo_client = pymongo.MongoClient(f"mongodb+srv://ismail:{MONGO_PASS}@hw1.m5wwlop.mongodb.net/?retryWrites=true&w=majority")
mongo_session = mongo_client.start_session()
mongo_db = mongo_client.main

def check_auth(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if 'username' not in session:
            session['result_msg'] = 'Auth Required'
            return redirect('/auth')
        else:
            return func(*args, **kwargs)

    return func_wrapper

def check_admin(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if session.get('username') != 'admin':
            session['result_msg'] = 'Not Permitted! Admin Role Required'
            return redirect('/auth')
        else:
            return func(*args, **kwargs)

    return func_wrapper

from modules.auth import auth_bp
from modules.controller import controller_bp
app.register_blueprint(auth_bp)
app.register_blueprint(controller_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)