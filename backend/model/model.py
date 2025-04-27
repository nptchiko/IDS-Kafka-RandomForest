#!/usr/bin/env python3
"""
Kafka-based ML Processor for Network Security
- Consumes Zeek logs from 'zeek-logs' Kafka topic
- Preprocesses data similar to continuous-ml-preprocessor.py
- Applies Random Forest model for prediction
- Produces alerts to 'alert' Kafka topic when malicious traffic is detected
"""

import json
import pickle
import pandas as pd
import numpy as np
import argparse
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer


class KafkaMLProcessor:
    def __init__(self, bootstrap_servers, input_topic, output_topic, model_path):
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.model_path = model_path

        # Load the ML model
        self.load_model()

        # Define features used in the model
        self.features = [
            'proto', 'service', 'id.resp_p', 'missed_bytes', 'version', 'cipher', 'curve',
            'resumed', 'established', 'sni_matches_cert'
        ]

        # Initialize Kafka consumer and producer
        self.init_kafka()

    def load_model(self):
        """Load the pickled Random Forest model."""
        try:
            self.model = pickle.load(open(self.model_path, 'rb'))
            print(f"Successfully loaded model from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def init_kafka(self):
        """Initialize Kafka consumer and producer."""
        try:
            self.consumer = KafkaConsumer(
                self.input_topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='latest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                group_id='ml-processor-group'
            )

            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )

            print(f"Connected to Kafka broker at {self.bootstrap_servers}")
            print(f"Consuming from topic: {self.input_topic}")
            print(f"Producing to topic: {self.output_topic}")

        except Exception as e:
            print(f"Error connecting to Kafka: {e}")
            raise

    def preprocess_log(self, log_entry):
        """Preprocess a single log entry for ML prediction."""
        try:
            # Convert single log entry to DataFrame

            df = pd.read_json(path_or_buf=log_entry, lines=True)
            print("hello")
            # Filter for features used in the model
            df = df[self.features].copy()

            # Clean and transform data
            df.replace(["", "-", "NULL"], pd.NA, inplace=True)
            df['id.resp_p'] = pd.to_numeric(
                df['id.resp_p'], errors='coerce').astype('Int64')
            df['missed_bytes'] = pd.to_numeric(
                df['missed_bytes'], errors='coerce').astype('Int64')

# df['username'] = np.where(
#     df['username'].notna(),
#     0,
#     1
# )

# df['password'] = np.where(
#     df['password'].notna(),
#     0,
#     1
# )

            df['version'] = np.where(
                df['version'].notna() & ~df['version'].isin(
                    ['TLSv1.2', 'TLSv1.3']),
                0,
                1
            )
            df['cipher'] = np.where(
                df['cipher'].notna() &
                df['cipher'].str.contains('AES', na=False).eq(False) &
                df['cipher'].str.contains('GCM', na=False).eq(False) &
                df['cipher'].str.contains('ChaCha20', na=False).eq(False),
                0,
                1
            )

            df['curve'] = np.where(
                df['curve'].notna() & df['curve'].isin(
                    ['secp256r1', 'secp384r1', 'secp521r1', 'x25519']),
                0,
                1
            )

            df['resumed'] = np.where(
                df['resumed'].notna() & df['resumed'] == 'T',
                0,
                1
            )

            df['established'] = np.where(
                df['established'].notna() & df['established'] == 'F',
                0,
                1
            )

            df['sni_matches_cert'] = np.where(
                df['sni_matches_cert'].notna() & df['sni_matches_cert'] == 'F',
                0,
                1
            )

            df['secure_label'] = np.where(
                ((df['service'] == 'dns') & (df['id.resp_p'] == 53)) |
                ((df['service'] == 'dhcp') & ((df['id.resp_p'] == 67) | (df['id.resp_p'] == 68))) |
                ((df['service'] == 'ntp') & (df['id.resp_p'] == 123)) |
                (df['proto'] == 'unknown_transport') |
                (df['missed_bytes'].notna() & (df['missed_bytes'] > 0)) |
                # (df['username'] == 0) |
                # (df['password'] == 0) |
                (df['version'] == 0) |
                (df['cipher'] == 0) |
                (df['curve'] == 0) |
                (df['resumed'] == 0) |
                (df['established'] == 0) |
                (df['sni_matches_cert'] == 0),

                0,  # Value if condition is True (insecure)
                1   # Value if condition is False (secure)
            )

            return df

        except Exception as e:
            print(f"Error preprocessing log entry: {e}")
            print(f"Problematic log entry: {log_entry}")
            return None

    def predict(self, df):
        """Make prediction using the Random Forest model."""
        try:
            # Make prediction
            prediction = self.model.predict(df)[0]

            # Get prediction probability
            probability = self.model.predict_proba(df)[0]

            return {
                'prediction': int(prediction),  # 0 = insecure, 1 = secure
                # Confidence of prediction
                'confidence': float(probability[int(prediction)])
            }

        except Exception as e:
            print(f"Error making prediction: {e}")
            return None

    def create_alert(self, log_entry, prediction_result):
        """Create alert message based on log entry and prediction."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': log_entry.get('id.orig_h', 'unknown'),
            'source_port': log_entry.get('id.orig_p', 'unknown'),
            'dest_ip': log_entry.get('id.resp_h', 'unknown'),
            'dest_port': log_entry.get('id.resp_p', 'unknown'),
            'protocol': log_entry.get('proto', 'unknown'),
            'service': log_entry.get('service', 'unknown'),
            'prediction': prediction_result['prediction'],
            'confidence': prediction_result['confidence'],
            'alert_type': 'secure' if prediction_result['prediction'] == 1 else 'malicious',
            'severity': 'low' if prediction_result['prediction'] == 1 else 'high',
            'original_log': log_entry
        }

        return alert

    def run(self):
        """Main processing loop to consume logs, predict, and produce alerts."""
        print("Starting Kafka ML processor. Press Ctrl+C to stop.")

        try:
            # Process messages
            for message in self.consumer:
                # try:
                #     log_entry = message.value
                #
                #     # Check if log entry has required fields
                #     if not all(feature in log_entry for feature in self.features):
                #         print(f"Skipping log entry - missing required fields")
                #         continue
                #
                #     # Preprocess log entry
                #     df = self.preprocess_log(log_entry)
                #     if df is None or df.empty:
                #         continue
                #
                #     # Make prediction
                #     prediction_result = self.predict(df)
                #     if prediction_result is None:
                #         continue
                #
                #     # Create alert
                #     alert = self.create_alert(log_entry, prediction_result)
                #
                #     # Only send alert if traffic is malicious (prediction = 0)
                #     if prediction_result['prediction'] == 0:
                #         self.producer.send(self.output_topic, alert)
                #         print(f"Alert sent: Malicious traffic detected from {alert['source_ip']}:{
                #               alert['source_port']} to {alert['dest_ip']}:{alert['dest_port']}")
                # except Exception as e:
                #     print(f"Error processing message: {e}")
                #     continue
                #
                self.producer.send(self.output_topic, {'sample': 'test'})
        except KeyboardInterrupt:
            print("\nProcessing stopped by user")

        finally:
            print("Closing Kafka connections")
            self.consumer.close()
            self.producer.close()


def main():
    parser = argparse.ArgumentParser(
        description="Kafka-based ML processor for network security.")
    parser.add_argument("-b", "--bootstrap-servers", default="localhost:9092",
                        help="Kafka bootstrap servers (default: localhost:9092)")
    parser.add_argument("-i", "--input-topic", default="zeek-logs",
                        help="Kafka topic for input Zeek logs (default: zeek-logs)")
    parser.add_argument("-o", "--output-topic", default="alert",
                        help="Kafka topic for output alerts (default: alert)")
    parser.add_argument("-m", "--model", default="random_forest_model.sav",
                        help="Path to pickled Random Forest model (default: random_forest_model.sav)")

    args = parser.parse_args()

    processor = KafkaMLProcessor(
        args.bootstrap_servers,
        args.input_topic,
        args.output_topic,
        args.model
    )
    processor.run()


if __name__ == "__main__":
    main()
