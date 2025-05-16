# 🛰️ Real time Intrusive Detecting System With Apache Kafka
![image](https://github.com/user-attachments/assets/e1308846-08a0-415d-9769-8c272479dcb9) 

## About
- Full-stack IDS implementing Machine Learning (Random Forest) using logs extracted from **Zeek** tool,  utilizes **Kafka** for logs streaming, uses **Decision Tree** classification to detect malicious traffic, stores predicted result in **MongoDB**, and displays results in a **React** dashboard.

- We use **Docker** as main tool to deploy and containerize our systems modules.


## 📦 System Pipeline Overview
![image](https://github.com/user-attachments/assets/6258fd8b-5261-4bc8-ab3d-2910496f7419)


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
- Docker & Docker Compose
- [LazyDocker](https://github.com/jesseduffield/lazydocker) (Recommend) 
---

## 🚀 Quick Start

### 1. Clone the project
```bash
git clone https://github.com/nptchiko/IDS-Kafka-RandomForest.git
cd IDS-Kafka-RandomForest
```
### 2. Grant permission and run script:

```
chmod +x run.sh
./run.sh
```
Verify if system started successfully:
```
docker ps
```
![image](https://github.com/user-attachments/assets/63c046d9-8801-4a5f-9084-555a33ec16e6)

Or using LazyDocker:
![image](https://github.com/user-attachments/assets/1d653d69-4b28-4cde-b7c8-aa2296cfc2df)

### 3. 💻 Monitoring Kafka Health
- Utilize available resource for Kafka UI, thanks to [Creator](https://github.com/provectus/kafka-ui)
- You can check current status of Kafka such as:
    - Topic:
  ![image](https://github.com/user-attachments/assets/6ea91639-cac2-42e6-bdc6-ddc75486e21b)
    - Consumer:
  ![image](https://github.com/user-attachments/assets/3eee8e82-719a-4e08-ad2c-e4618f787e3b)
    - Connectors:
  ![image](https://github.com/user-attachments/assets/e63e2378-57b1-4bc6-81f2-34c63474c352)


Visit: http://localhost:8088

### 4. Check MongoDB Health 
- Main collection is ***status_info***
- Check its documents by running:
```
docker exec -it mongoserver mongosh -u admin -p admin --authenticationDatabase admin
show collections
db.status_info.find().pretty()
```
### 5. Another service
- Use lazydocker to check their logs

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
