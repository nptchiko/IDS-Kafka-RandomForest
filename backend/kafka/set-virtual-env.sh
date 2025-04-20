#!/bin/bash

python3 -m venv venv

source venv/bin/activate

venv/bin/pip3 install -r requirements.txt

pip3 install confluent_kafka

pip3 install flask


# Run each manually
#venv/bin/python3 consumer/consumer.py

#open another terminal
#venv/bin/python3 producer/producer.py
