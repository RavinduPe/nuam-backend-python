from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.device_event import DeviceEvent
from app.services.websocket_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/device")
async def device_ws(websocket: WebSocket):
    await websocket.accept()
    db: Session = SessionLocal()

    try:
        while True:
            data = await websocket.receive_json()

            event = DeviceEvent(
                device_id=data["device_id"],
                event_type=data["event_type"]
            )

            db.add(event)
            db.commit()

            # Send event to frontend users
            await manager.broadcast(data)

    except WebSocketDisconnect:
        db.close()
