FROM python:3.9-slim

WORKDIR /model

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt 

COPY model.py .

COPY RandomForestModel.sav .

#ENV BOOTSTRAP_SERVERS=kafka:9092
#ENV INPUT_TOPIC=zeek-logs
#ENV OUTPUT_TOPIC=alert
#ENV MODEL_PATH=/app/RandomForestModel.sav

CMD ["sh", "-c", "python3 /app/model.py \
            -b $BOOTSTRAP_SERVERS \
            -i $INPUT_TOPIC \
            -o $OUTPUT_TOPIC \
            --model ${MODEL_PATH}"]



