FROM python:3.9-slim

WORKDIR /app

COPY zeek_merger.py /app/

RUN chmod +x /app/zeek_merger.py 

RUN mkdir -p /logs 

RUN pip3 install --no-cache-dir pandas pytest

COPY test_zeek_logs.py /app/
# RUN pytest /app/test_zeek_logs.py

ENTRYPOINT ["python3", "/app/zeek_merger.py"] 

