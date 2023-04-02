from flask import (Flask, session, request)
import pymongo
from os import environ

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# MONGO_PASS = environ.get('MONGO_PASS')
MONGO_PASS = "alperen60"
mongo_client = pymongo.MongoClient(f"mongodb+srv://ismail:{MONGO_PASS}@hw1.m5wwlop.mongodb.net/?retryWrites=true&w=majority")
mongo_session = mongo_client.start_session()
mongo_db = mongo_client.main

from modules.auth import auth_bp
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)