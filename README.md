# 🛰️ Real time Intrusive Detecting System With Apache Kafka
![image](https://github.com/user-attachments/assets/e1308846-08a0-415d-9769-8c272479dcb9) 

## About
- Full-stack IDS implementing Machine Learning (Random Forest) using logs extracted from **Zeek** tool,  utilizes **Kafka** for logs streaming, uses **Decision Tree** classification to detect malicious traffic, stores predicted result in **MongoDB**, and displays results in a **React** dashboard.

- We use **Docker** as main tool to deploy and containerize our systems modules.

## Thứ tự để chạy docker:

    zeek -> merge_logs -> db -> kafka -> kafka-connect script


## 📦 System Pipeline Overview

```
graph TD
    Zeek -->|Logs| Kafka --> PythonConsumer --> MongoDB
    PythonConsumer --> DecisionTree --> WebSocketServer
    WebSocketServer --> ReactFrontend
```

---

## 🗂️ Project Modules

- **Network capturing (Zeek)**  
  We use zeek to capture traffic in host interface, generate log files, merge it into dataset.json with needed logs and wait for Kafka Connector to transfer.

- **UI Frontend (React + TypeScript + Vite)**  
  Interactive UI with live updates via WebSocket.

- **Data Streaming (Kafka)**  
  -> Detail in here: [KAFKA README.md](./kafka/README.md)

- **ML Classification (Decision Tree)**  
  Classifies network traffic (e.g., Normal vs Malicious) consumed data from Kafka.

---

## ⚙️ System Requirements

- Node.js ≥ 18  
- Python ≥ 3.8  
- Docker & Docker Compose  
- MongoDB (via Docker)  
- Zeek (for log generation)  
- Kafka setup  
- `nvm` (optional for node version management)

---

## 🚀 Quick Start

### 1. Clone the project
```bash
git clone https://github.com/your-username/network-classifier.git
cd network-classifier
```


### 2. 🐳 Start MongoDB via Docker
Navigate to the MongoDB module:
cd backend/database
```
docker compose up -d
```
Verify:
```
docker ps -a
docker exec -it my-mongodb mongosh -u admin -p admin --authenticationDatabase admin
```
### 3. 🧠 Run ML Socket Server
Navigate to the socket server:


```
cd backend/socket_server
pip install -r requirements.txt
python3 server.py
```
This will open a socket at localhost:5000 that the frontend will connect to.

### 4. 💻 Start Frontend
Navigate to frontend folder:

```
cd frontend
nvm use 18 # or install node 18+
npm install
npm run dev
```
Visit: http://localhost:5173

### 🧬 Data Flow

```
graph TD
  Zeek -->|PCAP logs| Kafka
  Kafka --> MongoDB
  MongoDB --> FlaskSocketServer
  FlaskSocketServer --> ReactFrontend
  FlaskSocketServer -->|Classification| DecisionTree
  ```
### 🧪 Model: Decision Tree Classifier
Input: Transformed Zeek logs (e.g. conn.log)

Output: Class label (e.g., "benign", "malicious")

Model code located in /backend/socket_server/ml/decision_tree.py

### 🧹 Linting & Type Safety
- ESLint with type-aware config for production.

- Recommended plugins:

    - eslint-plugin-react-x

    - eslint-plugin-react-dom

### 🧩 Extending
🔐 Add JWT for user-based dashboards

📈 Add charts with recharts or chart.js

📡 Optionally push to cloud DB (e.g., MongoDB Atlas)

### 📜 License
MIT © 2025

### 🧑‍💻 Author
Created by:
    Quang Minh
    Vy Truong
    Phuoc Tien

Let me know if:
- You want this auto-split into 3 READMEs per folder.
- You need support for `docker-compose.yml` generation.
- You want the Mermaid diagram exported as SVG.
---
