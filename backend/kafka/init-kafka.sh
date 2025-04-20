#!/bin/bash

docker compose up -d

#create new topic
#this will create new topic with name of topic_name, 3 paritions, 1 copy
docker compose exec kafka kafka-topics --bootstrap-server kafka:9092 --topic zeek_logs --create --partitions 3 --replication-factor 1
