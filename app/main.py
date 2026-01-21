from fastapi import FastAPI
from app.api import device_ws, frontend_ws

app = FastAPI(title="Device Monitoring Backend")

app.include_router(device_ws.router)
app.include_router(frontend_ws.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Device Monitoring Backend!"}
