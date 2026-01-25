from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import WebSocketManager

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/ws/frontend")
async def frontend_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
