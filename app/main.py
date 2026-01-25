from fastapi import FastAPI, WebSocket
from app.api.device_ws import device_websocket
# from app.api.frontend_ws import frontend_websocket
from app.core.database import engine
from app.models.device_event import Base

app = FastAPI(title="Network Device Monitoring")

Base.metadata.create_all(bind=engine)

@app.websocket("/ws/device")
async def ws_device(websocket: WebSocket):
    await device_websocket(websocket)

# @app.websocket("/ws/frontend")
# async def ws_frontend(websocket: WebSocket):
#     await frontend_websocket(websocket)
