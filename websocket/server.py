
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


MONGO_URL = 'mongodb://admin:admin@localhost:27017/test?authSource=admin'
MONGO_DB = 'test'
COLLECTIONS = ["tls_pie_data", "status_info", "missed_bytes_data", "logs_data"]


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

    new_tls_pie = SocketService.extract_new_records("tls_pie_data", tls_pie_data)
    new_status_info = SocketService.extract_new_records("status_info", status_info)
    new_missed_bytes = SocketService.extract_new_records("missed_bytes_data", missed_bytes_data)
    new_logs = SocketService.extract_new_records("logs_data", logs_data)

    status_data = {
        'tlsPieData': tls_pie_data,
        'statusInfo': current_status,
        'missedBytesData': missed_bytes_data,
        'logsData': logs_data
    }
    print("\nStatus data: ", status_data)

    # Compare with previous data
    if SocketService.is_data_changed(status_data):
        if any([new_logs, new_tls_pie, new_missed_bytes, new_status_info]):
            status_data = {
                'tlsPieData': new_tls_pie,
                'statusInfo': new_status_info,
                'missedBytesData': new_missed_bytes,
                'logsData': new_logs
            }
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
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)