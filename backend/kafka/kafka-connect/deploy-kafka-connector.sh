#!/bin/bash

curl -X POST -H "Content-Type: application/json" --data @kafka-connect.json http://localhost:8083/connectors
