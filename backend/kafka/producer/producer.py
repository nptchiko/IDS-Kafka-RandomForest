from confluent_kafka import Producer
from json import dumps
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

kafka_config = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'zeek-producer'
}

producer = Producer(kafka_config)
topic = 'zeek_logs'


def delivery_result(err, msg):
    if err is not None:
        print(f"Message sent failed; {err}")
    else:
        print(f"Message sent to {msg.topic()} [{msg.partition()}]")


def send_kafka(data: dict):
    try:
        producer.produce(
            topic,
            key=data.get('key'),
            value=data.get('value'),
            callback=delivery_result
        )
        producer.poll(0)
        return {"stauts": "success"}
    except Exception as e:
        print(f"Error in sending: {e}")


def take_input():
    data: dict = {}
    data['key'] = input('key: ')
    data['value'] = input('value: ')

    return data


@app.route('/health')
def health():
    return jsonify({"status": "healthy",
                    "kafka_brokers": kafka_config['bootstrap.servers']})


@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        key = request.form.get('key')
        value = request.form.get('value')

        send_kafka(data={'key': key, 'value': value})

    return '''
           <form method="POST">
               <div><label>Key: <input type="text" name="key"></label></div>
               <div><label>Value: <input type="text" name="value"></label></div>
               <input type="submit" value="Send">
           </form>'''


@app.route('/test')
def test():
    return send_kafka(data={'key': 'id', 'value': '123'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
