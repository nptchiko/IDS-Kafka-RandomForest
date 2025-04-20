from flask import Flask, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime
import logging
from bson import ObjectId
import threading


app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")


MONGO_URL = 'mongodb://admin:admin@localhost:27017/test'
MONGO_DB = 'test'
MONGO_COLLECTION = 'processed_data'

@socketio.on('connect')
def connect_server(auth=None): 
    # socketio.emit("initial_data",initial_data)
    print("connected")

@socketio.on('refresh')
def update_data(auth=None): 
    updated_data = str(input())
    socketio.emit("update_data",updated_data,  broadcast=True)

if __name__ == "__main__":
    connect_server()
    update_data()