from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.device_event import DeviceEvent
from app.schemas.device_event import DeviceEventCreate
from app.services.websocket_manager import manager

async def device_websocket(websocket: WebSocket):
    await websocket.accept()
    db: Session = SessionLocal()

    try:
        while True:
            data = await websocket.receive_json()
            event = DeviceEventCreate(**data)

            db_event = DeviceEvent(
                device_id=event.device_id,
                event_type=event.event_type,
                uptime=event.uptime,
                traffic=event.traffic
            )

            db.add(db_event)
            db.commit()

            # Broadcast to frontend
            await manager.broadcast(data)

    except WebSocketDisconnect:
        print("Device service disconnected")
    finally:
        db.close()
