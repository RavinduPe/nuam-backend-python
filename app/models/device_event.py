from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class DeviceEvent(Base):
    __tablename__ = "device_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    event_type = Column(String)  # connect / disconnect / metric
    uptime = Column(Float, nullable=True)
    traffic = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
