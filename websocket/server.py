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
# MONGO_COLLECTION = 'processed_data'

@app.route('/')
def health_check():
    return jsonify({"status": "running"}), 200

def fetch_mongo_data(collection_name):
    try:
        client = MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        collection = db[collection_name]
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
    tls_pie_data = fetch_mongo_data("tls_pie_data")
    status_info = fetch_mongo_data("status_info")
    missed_bytes_data = fetch_mongo_data("missed_bytes_data")
    logs_data = fetch_mongo_data("logs_data")

    print("\nTLS Pie Data:", tls_pie_data)
    print("\nMissed Bytes Data:", missed_bytes_data)
    print("\nLogs Data:", logs_data)
    current_status = None
    if status_info and len(status_info) > 0 and 'current_status' in status_info[0]:
        print("\nStatus info:", status_info[0])
        current_status = status_info[0]['current_status']
    else:
        print("Warning: Could not retrieve 'current_status' from status_info.")

    initial_data = {
        'tlsPieData': tls_pie_data,
        'statusInfo': current_status,
        'missedBytesData': missed_bytes_data,
        'logsData': logs_data
    }
    print("\nInitial data: ", initial_data)

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