FROM python:3.9-slim

WORKDIR /app

COPY zeek_json_merger_continuous.py /app/

RUN chmod +x /app/zeek_json_merger_continuous.py

RUN mkdir -p /logs

ENTRYPOINT ["python3", "/app/zeek_json_merger_continuous.py"]

CMD ["--help"]
