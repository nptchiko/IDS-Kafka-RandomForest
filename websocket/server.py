
from flask import Flask, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime
# import logging
from bson import ObjectId
import threading


app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")


MONGO_URL = 'mongodb://admin:admin@localhost:27017/test?authSource=admin'
MONGO_DB = 'test'
# MONGO_COLLECTION = 'processed_data'


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
    updated_data = watch_mongo_changes()
    socketio.emit("update_data",updated_data,  broadcast=True)
    print("Refresh ", updated_data)

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
