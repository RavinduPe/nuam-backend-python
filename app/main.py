from fastapi import FastAPI, WebSocket, Depends,WebSocketDisconnect
from app.core.database import SessionLocal
from app.api.frontend_ws import frontend_ws
from app.core.database import engine, get_db
from app.models.device_event import Base
from app.models.device_event import DeviceEvent
from sqlalchemy.orm import Session
from app.services.websocket_manager import manager
from app.services.event_processor import EventProcessor

from datetime import datetime
import json

app = FastAPI(title="Network Device Monitoring")

Base.metadata.create_all(bind=engine)

@app.get("/device-events")
def get_device_events(db: Session = Depends(get_db)):
    device_events = db.query(DeviceEvent).all()
    return device_events

@app.websocket("/ws/device")
async def device_ws(websocket: WebSocket):
    await manager.connect(websocket)

    db = SessionLocal()
    processor = EventProcessor(db)

    try:
        while True:
            data = await websocket.receive_json()

            # SAVE TO DATABASE
            processor.process_event(data)

            # BROADCAST TO FRONTEND
            await manager.broadcast(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)



@app.websocket("/ws/frontend")
async def ws_frontend(websocket: WebSocket):
    await frontend_ws(websocket)
