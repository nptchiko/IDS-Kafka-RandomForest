
from flask import Flask, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime
# import logging
from bson import ObjectId
import threading


app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")


MONGO_URL = 'mongodb://admin:admin@localhost:27017/test'
MONGO_DB = 'test'
MONGO_COLLECTION = 'processed_data'


@app.route('/')
def health_check():
    return jsonify({"status": "running"}), 200

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [objectid_to_str(item) for item in obj]
    else:
        return obj

def fetch_mongo_data():
    try:
        client = MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        data = list(collection.find())
        data = objectid_to_str(data)
        
        return data
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        return []
    finally:
        client.close()

def watch_mongo_changes():
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    with collection.watch() as stream:
        for change in stream:
            print('MongoDB change detected:', change)
            updated_data = fetch_mongo_data()  
            socketio.emit("update_data",updated_data,  broadcast=True)

def start_change_stream():
    threading.Thread(target=watch_mongo_changes, daemon=True).start()

@socketio.on('connect')
def handle_connect(auth=None): 
    initial_data = fetch_mongo_data()
    socketio.emit("initial_data",initial_data)
    print("Connect ", initial_data)


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('refresh')
def handle_refresh():
    updated_data = watch_mongo_changes()
    socketio.emit("update_data",updated_data,  broadcast=True)
    print("Refresh ", updated_data)

if __name__ == '__main__':
    print("Server starting")
    # threading.Thread(target=watch_mongo_changes, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)