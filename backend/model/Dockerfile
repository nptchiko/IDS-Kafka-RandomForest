FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY model.py .
COPY RandomForestModel.sav .


ENV BOOTSTRAP_SERVERS=kafka:9092
ENV INPUT_TOPIC=zeek-logs
ENV OUTPUT_TOPIC=alert
ENV MODEL_PATH=RandomForestModel.sav

CMD ["python", "model.py", \
     "--bootstrap-servers", "${BOOTSTRAP_SERVERS}", \
     "--input-topic", "${INPUT_TOPIC}", \
     "--output-topic", "${OUTPUT_TOPIC}", \
     "--model", "${MODEL_PATH}"]
