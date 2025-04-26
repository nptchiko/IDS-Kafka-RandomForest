#!/bin/bash

# sleep 10
# Run docker-compose
docker-compose up

# Copy from container to host
docker cp zeek_container:/conn.log ./logs/
docker cp zeek_container:/http.log ./logs/
docker cp zeek_container:/ssl.log ./logs/
docker cp zeek_container:/x509.log ./logs/

