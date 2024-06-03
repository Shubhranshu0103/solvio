from flask import Flask
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://shubhranshusinghwork:kjtAkTbt7uo2yEcd@solviodb.sjawyxf.mongodb.net/solvio?retryWrites=true&w=majority&appName=SolvioDB"

# setup mongodb connection
db = PyMongo(app).db

from application import routes
