import json
import pickle
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timezone
from kafka import KafkaConsumer, KafkaProducer
from io import StringIO


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
            'missed_bytes', 'version', 'cipher', 'curve', 'resumed', 'last_alert', 'established', 'sni_matches_cert', 'username', 'password',
            'certificate.not_valid_before', 'certificate.not_valid_after', 'certificate.sig_alg', 'certificate.key_length', 'certificate.key'
        ]

        print("kafka bootstrap server: " + self.bootstrap_servers)
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

            df = pd.read_json(path_or_buf=StringIO(log_entry), lines=True)

            # Filter for features used in the model
            df = df[self.features].copy()

            df.replace(["", "-", "NULL"], pd.NA, inplace=True)

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

            df['certificate.sig_alg'] = np.where(
                df['certificate.sig_alg'].notna() & ~df['certificate.sig_alg'].isin([
                    'sha256WithRSAEncryption',
                    'sha384WithRSAEncryption',
                    'sha512WithRSAEncryption',
                    'ecdsa-with-SHA256',
                    'ecdsa-with-SHA384',
                    'ecdsa-with-SHA512',
                    'rsassaPss',  # Generally secure but ideally we'd check parameters
                    'ed25519',
                    'ed448'
                ]),
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

            return df

        except Exception as e:
            print(f"Error preprocessing log entry: {e}")
            print(f"Problematic log entry: {log_entry}")
            return None

    def predict(self, df):
        """Make prediction using the Random Forest model."""
        try:
            # Make prediction
            df.to_csv('clean_dataset.csv')
            df = pd.read_csv('./clean_dataset.csv')
            df = df.drop([
                'Unnamed: 0'
            ], axis=1)

            prediction = self.model.predict(df)[0]

            # Get prediction probability

            return {
                'prediction': int(prediction)
                # 0 = insecure, 1 = secure
                # Confidence of prediction

            }

        except Exception as e:
            print(f"Error making prediction: {e}")
            return None

    def create_alert(self, log_entry, prediction_result):
        """Create alert message based on log entry and prediction."""
        log = json.loads(log_entry)
        alert = {
            'time': datetime.now(timezone.utc).astimezone().strftime("%X"),
            'current_status': 'safe' if prediction_result['prediction'] == 1 else 'unsafe',
            'status': 'Safe' if prediction_result['prediction'] == 1 else 'Unsafe',
            'missed_bytes': 0 if log['missed_bytes'] is None else log['missed_bytes'],
            "proto": log['proto'],
            "version": log['version'],
            "id.orig_h": log['id.orig_h'],
            "id.resp_h": log['id.resp_h'],
        }

        return alert

    def run(self):
        """Main processing loop to consume logs, predict, and produce alerts."""
        print("Starting Kafka ML processor. Press Ctrl+C to stop.")

        try:
            # Process messages
            for message in self.consumer:
                try:
                    log_entry = message.value
                    print('log entry type', type(log_entry))
                    # Check if log entry has required fields
                    if not all(feature in log_entry for feature in self.features):
                        print(f"Skipping log entry - missing required fields")
                        continue

                    # Preprocess log entry
                    df = self.preprocess_log(log_entry)
                    if df is None or df.empty:
                        print(log_entry)
                        print("Cant process logentry")
                        continue

                    # Make prediction
                    prediction_result = self.predict(df)
                    if prediction_result is None:
                        print("prediction failed!")
                        continue

                    # Create alert
                    alert = self.create_alert(log_entry, prediction_result)

                    # Only send alert if traffic is malicious (prediction = 0)
                    self.producer.send(self.output_topic, alert)
                    print(f"""Message produced at {alert['time']} with  result {
                          alert['current_status']}""")

                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue
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