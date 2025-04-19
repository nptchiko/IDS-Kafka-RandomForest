from confluent_kafka import Consumer, Producer
from flask import Flask, jsonify
from flask_socketio import SocketIO
import json
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest
import numpy as np
from datetime import datetime, timedelta
import logging
from bson import ObjectId
# import eventlet

# eventlet.monkey_patch()

app = Flask(__name__)
logging.getLogger('socketio').setLevel(logging.DEBUG)
logging.getLogger('engineio').setLevel(logging.DEBUG)

socketio = SocketIO(app, cors_allowed_origins="*")


MONGO_URL = 'mongodb://admin:admin@localhost:27017/test?authSource=admin'
MONGO_DB = 'test'
MONGO_COLLECTION = 'processed_data'

@app.route('/')
def health_check():
    return jsonify({"status": "running"}), 200

def fetch_mongo_data():
    try:
        client = MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        data = list(collection.find({}))

        # Convert ObjectId to str
        for doc in data:
            doc["_id"] = str(doc["_id"])
        
        print(f"Successfully fetched {len(data)} records from MongoDB")
        return data
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        return []
    finally:
        client.close()

@socketio.on('connect')
def handle_connect(auth=None):
    print("Client connected")   
    initial_data = fetch_mongo_data()
    print(f"Fetched initial data: {initial_data}")
    socketio.emit('initial_data', {'data': initial_data})
    print("Emitted initial_data event")


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('refresh')
def handle_refresh():
    print("Client requested data refresh")
    updated_data = fetch_mongo_data()
    socketio.emit('updated_data', {'data': updated_data})

# test emit dataa
# def background_emit():
#     count = 0
#     while True:
#         count += 1
#         data = {'message': f"Hello {count}", 'timestamp': time.time()}
#         socketio.emit('realtime_data', data)

if __name__ == '__main__':
    print("Server starting")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)