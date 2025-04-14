from confluent_kafka import Producer
import json
import os
from merge_logs import merge_logs

conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'zeek-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def process_zeek_logs(zeek_logs_dir):
    try:
        merged_df = merge_logs(zeek_logs_dir)
    except Exception as e:
        print(f"Error merging logs: {e}")
        return
    
    for _, row in merged_df.iterrows():
        log_entry = row.to_dict()
        message = json.dumps(log_entry)
        producer.produce('zeek_logs_topic', value=message.encode('utf-8'), callback=delivery_report)
        producer.poll(0)

    producer.flush()

if __name__ == '__main__':
    zeek_logs_dir = 'zeek_logs'
    if os.path.exists(zeek_logs_dir):
        process_zeek_logs(zeek_logs_dir)
    else:
        print(f"Zeek logs directory {zeek_logs_dir} not found. Run Zeek first.")