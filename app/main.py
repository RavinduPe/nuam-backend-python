from fastapi import FastAPI, WebSocket, Depends,WebSocketDisconnect
from app.core.database import SessionLocal
from app.api.frontend_ws import frontend_ws
from app.core.database import engine, get_db
from app.models.device_event import Base
from app.models.device_event import DeviceEvent
from sqlalchemy.orm import Session
from app.services.websocket_manager import manager
from app.services.event_processor import EventProcessor
from app.services.report_service import ReportService

from datetime import datetime
import json

app = FastAPI(title="Network Device Monitoring")

Base.metadata.create_all(bind=engine)

@app.get("/reports/daily")
def get_daily_report(date: str = None, db: Session = Depends(get_db)):
    report_service = ReportService(db)
    if date:
        report_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        report_date = None

    report = report_service.generate_daily_report(report_date)
    return report

@app.get("/reports/daily/excel")
def download_daily_report(date: str = None, db: Session = Depends(get_db)):
    report_service = ReportService(db)
    if date:
        report_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        report_date = None

    report = report_service.generate_daily_report(report_date)
    filepath = report_service.save_report_excel(report)
    return {"file_path": filepath, "message": "Excel report generated successfully"}

@app.websocket("/ws/device")
async def device_ws(websocket: WebSocket):
    await manager.connect(websocket)

    db = SessionLocal()
    processor = EventProcessor(db)

    try:
        while True:
            data = await websocket.receive_json()

            # Save event to DB
            processor.process_event(data)

            # Calculate dashboard stats
            stats = processor.get_dashboard_stats()

            # Attach stats to outgoing message
            enriched_data = {
                "event": data,
                "dashboard_stats": stats
            }

            # Broadcast enriched message
            await manager.broadcast(enriched_data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)



@app.websocket("/ws/frontend")
async def ws_frontend(websocket: WebSocket):
    await frontend_ws(websocket)
