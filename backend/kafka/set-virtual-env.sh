#!/bin/bash

python -m venv venv

source venv/bin/activate

venv/bin/pip3 install -r requirements.txt

# Run each manually
#venv/bin/python3 consumer/consumer.py

#open another terminal
#venv/bin/python3 producer/producer.py
