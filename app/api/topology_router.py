from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import asyncio

from app.core.database import get_db
from app.models.device import Device

router = APIRouter(prefix="/api/topology", tags=["Topology"])


# Helper Functions
def map_device_type(db_type: str | None) -> str:
    mapping = {
        "LAPTOP": "laptop",
        "MOBILE": "mobile",
        "PRINTER": "printer",
        "IOT": "iot",
        "NETWORK": "network"
    }
    return mapping.get(db_type, "network")


def calculate_status(last_seen: datetime | None) -> str:
    if not last_seen:
        return "offline"

    # Make last_seen timezone-aware if naive
    if last_seen.tzinfo is None:
        last_seen = last_seen.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    diff = (now - last_seen).total_seconds()

    if diff < 60:
        return "active"
    elif diff < 300:
        return "idle"
    else:
        return "offline"


def calculate_activity(last_seen: datetime | None) -> str:
    if not last_seen:
        return "low"

    if last_seen.tzinfo is None:
        last_seen = last_seen.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    diff = (now - last_seen).total_seconds()

    if diff < 30:
        return "high"
    elif diff < 120:
        return "medium"
    else:
        return "low"    


def build_topology_response(db: Session):
    devices = db.query(Device).all()

    device_list = []

    for d in devices:
        status = calculate_status(d.last_seen)
        activity = calculate_activity(d.last_seen)

        device_list.append({
            "id": d.device_id,
            "name": d.hostname or d.device_id,
            "ip": d.ip_address,
            "mac": d.device_id,
            "vendor": d.vendor,
            "type": map_device_type(d.device_type),
            "status": status,
            "firstSeen": d.first_seen.isoformat() if d.first_seen else None,
            "lastSeen": d.last_seen.isoformat() if d.last_seen else None,
            "activityLevel": activity
        })

    return {
        "switch": {
            "id": "core-switch-1",
            "name": "Core Switch",
            "status": "healthy",
            "x": 400,
            "y": 300
        },
        "devices": device_list
    }


# REST Endpoint
@router.get("/")
def get_topology(db: Session = Depends(get_db)):
    return build_topology_response(db)


# WebSocket Endpoint
@router.websocket("/ws")
async def topology_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = build_topology_response(db)
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected")