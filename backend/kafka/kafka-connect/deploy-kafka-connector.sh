#!/bin/bash

echo -ne "\n\nWaiting for the systems to be ready.."
sleep 7

echo -e "\nAdding Log Streaming Connector for the 'zeek-logs' topic:"
curl -X POST -H "Content-Type: application/json" --data '@log-streaming-connect.json' http://localhost:8083/connectors

sleep 2
echo -e "\nAdding MongoDB Kafka Sink Connector for the 'alert' topic into the 'test.alert' collection:"
curl -X POST -H "Content-Type: application/json" --data '@alert-sink.json' http://localhost:8083/connectors
