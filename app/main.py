from fastapi import FastAPI, WebSocket, Depends,WebSocketDisconnect
from app.core.database import SessionLocal
from app.api.frontend_ws import frontend_ws
from app.core.database import engine, get_db
from app.models.device_event import Base
from app.models.device_event import Device, DeviceEvent
from sqlalchemy.orm import Session

from datetime import datetime
import json

app = FastAPI(title="Network Device Monitoring")

Base.metadata.create_all(bind=engine)

@app.get("/device-events")
def get_device_events(db: Session = Depends(get_db)):
    device_events = db.query(DeviceEvent).all()
    return device_events

@app.websocket("/ws/device")
async def device_ws(ws: WebSocket):
    await ws.accept()
    db = SessionLocal()

    try:
        while True:
            raw = await ws.receive_text()
            event = json.loads(raw)

            print("[DEVICE EVENT]", event)

            # ---- store raw event ----
            meta = event.get("meta", {})
            payload = event.get("payload", {})

            db_event = DeviceEvent(
                event_type=payload.get("event_type"),
                timestamp=datetime.fromisoformat(
                    payload.get("timestamp").replace("Z", "+00:00")
                ),
                sequence=meta.get("sequence"),
                payload=payload
            )
            db.add(db_event)

            # ---- update device table ----
            device_data = payload.get("device", {})
            mac = device_data.get("device_id")

            if mac:
                device = db.query(Device).filter(Device.mac == mac).first()
                if not device:
                    device = Device(mac=mac)
                    db.add(device)

                device.ip_address = device_data.get("ip_address")
                device.hostname = device_data.get("hostname")
                device.device_type = device_data.get("device_type")
                device.vendor = device_data.get("vendor")
                device.os = device_data.get("os")
                device.first_seen = datetime.fromisoformat(
                    device_data.get("first_seen").replace("Z", "+00:00")
                )
                device.last_seen = datetime.fromisoformat(
                    device_data.get("last_seen").replace("Z", "+00:00")
                )
                device.status = payload.get("event_type")

            db.commit()

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        db.close()



@app.websocket("/ws/frontend")
async def ws_frontend(websocket: WebSocket):
    await frontend_ws(websocket)
