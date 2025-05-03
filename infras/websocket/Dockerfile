FROM python:3.9-slim


WORKDIR /websocket

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# EXPOSE 5000

# ENV FLASK_APP=server.py
ENV FLASK_ENV=production

CMD ["python", "server.py"]