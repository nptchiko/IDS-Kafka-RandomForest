# Network Security Monitoring System

A comprehensive network security monitoring system that uses Zeek logs, Kafka streaming, and machine learning to detect malicious network traffic in real-time.

## System Overview

This system continuously processes Zeek network logs, applies machine learning techniques to identify potentially malicious traffic, and generates alerts. The pipeline includes:

1. **Zeek Network Monitor**: Captures and logs network traffic
2. **Kafka Integration**: Streams logs for real-time processing
3. **ML Preprocessing**: Cleans and transforms raw logs for ML input
4. **Random Forest Model**: Classifies traffic as secure or malicious
5. **Alert System**: Generates and routes security alerts

## Architecture

```
┌───────────┐    ┌───────────┐    ┌────────────┐    ┌──────────┐    ┌──────────┐
│  Network  │━━━▶│    Zeek   │━━━▶│  Kafka     │━━━▶│  ML      │━━━▶│  Alert   │
│  Traffic  │    │  Monitor  │    │(zeek-logs) │    │Processor │    │  System  │
└───────────┘    └───────────┘    └────────────┘    └──────────┘    └──────────┘
```

## Components

### Zeek Monitor

[Zeek](https://zeek.org/) (formerly Bro) monitors network traffic and generates detailed logs of network activity. These logs are stored in JSON format and merged into a single file for processing.

### Continuous Data Preprocessor

The `continuous-ml-preprocessor.py` script:
- Monitors Zeek merged log files
- Cleans and transforms raw data
- Prepares features for the machine learning model
- Generates a labeled dataset with secure/insecure classifications

### Kafka ML Processor

The `kafka_ml_processor.py` script:
- Consumes log records from the Zeek-logs Kafka topic
- Preprocesses and transforms each record
- Applies the trained Random Forest model for prediction
- Produces alert messages to the alert Kafka topic when threats are detected

## Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.7+
- Kafka
- Zeek Network Monitor

### Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/network-security-monitoring.git
   cd network-security-monitoring
   ```

2. Build the Docker containers:
   ```
   docker-compose build
   ```

3. Start the system:
   ```
   docker-compose up -d
   ```

### Configuration

Each component can be configured through environment variables or command-line arguments:

#### Continuous ML Preprocessor
```
python continuous-ml-preprocessor.py --input /path/to/merged.log --output clean_dataset.csv --interval 10
```

#### Kafka ML Processor
```
python kafka_ml_processor.py --bootstrap-servers kafka:9092 --input-topic zeek-logs --output-topic alert --model random_forest_model.sav
```

## Model Training

The system uses a Random Forest model to classify network traffic. To train the model:

1. Generate a clean dataset using the preprocessor:
   ```
   python continuous-ml-preprocessor.py --input /path/to/merged.log --output training_data.csv
   ```

2. Train the model using the training script (not included in this repo):
   ```
   python train_random_forest.py --input training_data.csv --output random_forest_model.sav
   ```

## Traffic Classification Rules

The system classifies traffic as potentially malicious based on these indicators:

- Non-standard DNS, DHCP, or NTP traffic
- Unknown transport protocols
- Missing bytes in transmission
- Outdated TLS versions (below TLSv1.2)
- Weak encryption ciphers
- Unusual elliptic curves
- Connection issues (resumed/established)
- SNI certificate mismatches

## Alert Format

Alerts are JSON objects with the following structure:
```json
{
  "timestamp": "2025-04-28T10:15:30.123456",
  "source_ip": "192.168.1.100",
  "source_port": 12345,
  "dest_ip": "10.0.0.1",
  "dest_port": 443,
  "protocol": "tcp",
  "service": "ssl",
  "prediction": 0,
  "confidence": 0.95,
  "alert_type": "malicious",
  "severity": "high",
  "original_log": { ... }
}
```

## System Requirements

- CPU: 4+ cores recommended
- RAM: 8GB+ recommended
- Storage: 100GB+ for log storage
- Network: 1Gbps Ethernet

## Troubleshooting

### Common Issues

- **Kafka connection errors**: Verify Kafka broker is running and accessible
- **Missing Zeek logs**: Check Zeek configuration and ensure logs are being written
- **Model loading errors**: Verify model file path and format

### Logging

Each component logs to standard output, which can be viewed with:
```
docker-compose logs -f [service-name]
```

## License

[Your License Here]

## Contributors

[Your Name/Organization]
