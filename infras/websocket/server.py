
from flask import Flask, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime
import logging
from bson import ObjectId
from socket_service import SocketService

app = Flask(__name__)
logging.getLogger('socketio').setLevel(logging.DEBUG)
logging.getLogger('engineio').setLevel(logging.DEBUG)

socketio = SocketIO(app, cors_allowed_origins="*")


MONGO_URL = 'mongodb://admin:admin@mongodb:27017/test?authSource=admin'
MONGO_DB = 'test'


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


def emit_data():
    status_info = fetch_mongo_data("status_info")

    print("\nNumber of data in mongo: ", len(status_info))

    new_status_info = SocketService.extract_new_records(
        "status_info", status_info)

    status_data = {
        'statusInfo': new_status_info,
    }

    print("New status data: ", len(status_data['statusInfo']))

    # Compare with previous data
    if SocketService.is_data_changed(status_data):
        socketio.emit('status_data', {'data': status_data})
        print("Data was changed, emit new data")
    else:
        print("No data change.")

def poll_mongo_changes():
    while True:
        try:
            emit_data()
            socketio.sleep(5)
        except Exception as e:
            print(f"Polling error: {e}")
            socketio.sleep(5)


def polling_watch():
    socketio.start_background_task(poll_mongo_changes)


@socketio.on('connect')
def handle_connect(auth=None):
    print("Client connected")
    # emit_data()
    polling_watch()


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")


@socketio.on('refresh')
def handle_refresh():
    updated_data = fetch_mongo_data()
    socketio.emit('updated_data', {'data': updated_data})


if __name__ == '__main__':
    print("Server starting")
    socketio.run(app, host='0.0.0.0', port=5000,
                 debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
