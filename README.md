# 🚀 Real-Time Device Monitoring Backend

A FastAPI-based backend system for real-time device connection monitoring using **WebSockets** and **SQLite**.
This backend receives device connect/disconnect events, stores them in the database, and broadcasts live updates to frontend clients (React).

---

## 📌 Project Features

* ✅ FastAPI backend
* ✅ WebSocket communication
* ✅ Device connect / disconnect detection
* ✅ Real-time event broadcasting
* ✅ SQLite database integration
* ✅ Clean project structure
* ✅ Ready for React frontend

---

## 🏗️ System Architecture

```
Device Service
     │
     │  WebSocket
     ▼
FastAPI Backend
     │
     ├── SQLite (event storage)
     │
     │  WebSocket
     ▼
React Frontend
```

---

## 📁 Project Structure

```
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── device_event.py
│   │
│   ├── schemas/
│   │   └── device_event.py
│   │
│   ├── services/
│   │   └── websocket_manager.py
│   │
│   └── api/
│       ├── device_ws.py
│       └── frontend_ws.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **WebSocket:** Starlette WebSocket
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Frontend:** React (WebSocket client)
* **Language:** Python 3.11 / 3.12

---

## 📦 Requirements

* Python 3.11+
* SQLite
* pip
* Virtual environment (recommended)

---

## 🔧 Installation

### 1️⃣ Clone repository

```bash
git clone <your-repo-url>
cd backend
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment variables

Create `.env` file:



---

### 5️⃣ Run the server

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 🔌 WebSocket Endpoints

### ▶ Device → Backend

```
ws://localhost:8000/ws/device
```

---

### ▶ Frontend → Backend

```
ws://localhost:8000/ws/frontend
```

Receives real-time device events.

---

## 🧪 WebSocket Test (Browser)

Open browser console:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/frontend");

ws.onopen = () => {
  console.log("Connected to backend");
};

ws.onmessage = (event) => {
  console.log("Live event:", event.data);
};

```

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for the full text.
