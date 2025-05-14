#!/bin/bash

echo 'Check to stop composing docker'
docker compose down --remove-orphans --volumes

sleep 1

echo 'Start to run docker compose...'
docker compose up -d

sleep 1

echo 'Add kafka connector...'
cd ./kafka/kafka-connect/ && ./deploy-kafka-connector.sh
