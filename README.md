🚨 Smart Disaster Response System
**A Containerized Real-Time Geospatial Monitoring Pipeline**


## 📖 Overview
This project is a full-stack, microservices-based disaster monitoring system. It simulates real-time disaster events (earthquakes, floods, etc.), ingests them through a high-performance **FastAPI** backend, stores them in **MongoDB**, and visualizes the results on an interactive **Leaflet.js** map with pulsing radar animations.

The entire infrastructure is orchestrated using **Docker**, ensuring environment parity and seamless deployment.

---

## 🛠️ Tech Stack
* **Backend:** Python 3.11, FastAPI (Asynchronous API)
* **Database:** MongoDB (NoSQL Persistence)
* **DevOps:** Docker, Docker Compose
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Leaflet.js
* **Integrations:** Telegram Bot API (Automated Alerts)

---

## 🏗️ System Architecture
The system is decoupled into three primary services:
1.  **Simulator:** A Python service that generates geo-fenced disaster data and dispatches POST requests.
2.  **API Gateway (Backend):** A containerized FastAPI service that handles data validation and database orchestration.
3.  **Persistence Layer:** A MongoDB container managing real-time data storage.
4.  **Observer (Frontend):** A web-based dashboard that polls the API and renders spatial data.

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
* Docker & Docker Compose installed.
* Python 3.x (for the simulator).

1. Launch the Infrastructure
docker-compose up -d
<img width="1919" height="1029" alt="DockerCompose and Simulator_CMD" src="https://github.com/user-attachments/assets/c4dc0bd2-ccad-494d-9466-1aa95e807404" />

2. Start the Data Stream
# Install dependencies
pip install -r simulator/requirements.txt

3. Run simulator
python simulator/sim.py
<img width="1919" height="1029" alt="DockerCompose and Simulator_CMD" src="https://github.com/user-attachments/assets/58e0f58f-6a27-46f1-b7b5-310ac3563a55" />

4. Watch the map
https://superpiyushv1.github.io/disaster-response-system/
<img width="1919" height="932" alt="DisasterMap_Frontend" src="https://github.com/user-attachments/assets/09ff89b3-ee3e-4890-bf3a-14328a0f13c1" />

5. Simultaneous Alerts on Telegram
6. <img width="1176" height="1029" alt="Telegram_Alerts" src="https://github.com/user-attachments/assets/9447b589-1068-4dbb-b282-767ee22668b1" />

