from confluent_kafka import Consumer
from json import dumps
import json
from flask import Flask, jsonify, render_template, Response
import queue
import threading

app = Flask(__name__)

kafka_config = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': "demo",
    'auto.offset.reset': 'latest'  # show message which is sent from now
}

consumer = Consumer(kafka_config)
topic = ['zeek_logs']
consumer.subscribe(topic)

message_queue = queue.Queue()


def consume_message():
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        print(msg.value())
#        key = msg.key().decode('utf-8') if msg.key() else 'unknown'
#        value = json.loads(msg.value().decode('utf-8'))
        key = msg.key() if msg.key() else 'unknown'
        value = msg.value()

        message_data = {
            'key': key,
            'value': value
        }
        message_queue.put(message_data)


threading.Thread(target=consume_message, daemon=True).start()


@app.route('/')
def stream():
    def event_stream():
        while True:
            try:
                message = message_queue.get(timeout=1)
                yield f"data: {message}\n\n"
            except queue.Empty:
                yield f"waiting\n\n"  # Keep connection alive
    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/health')
def health():
    return jsonify({"status": "healthy",
                    "kafka_brokers": kafka_config['bootstrap.servers']})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
