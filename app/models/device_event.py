from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class DeviceEvent(Base):
    __tablename__ = "device_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
