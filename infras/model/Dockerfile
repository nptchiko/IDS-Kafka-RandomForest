FROM python:3.9-slim

WORKDIR /model

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt 

COPY model.py .

RUN mkdir -p model

COPY RandomForestModel.sav model/

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

#ENV BOOTSTRAP_SERVERS=kafka:9092
#ENV INPUT_TOPIC=zeek-logs
#ENV OUTPUT_TOPIC=alert
#ENV MODEL_PATH=/app/RandomForestModel.sav

CMD ["./entrypoint.sh"]



