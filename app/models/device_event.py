from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.core.database import Base

class Device(Base):
    __tablename__ = "devices"

    mac = Column(String, primary_key=True, index=True)
    ip_address = Column(String)
    hostname = Column(String)
    device_type = Column(String)
    vendor = Column(String)
    os = Column(String)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    status = Column(String)

class DeviceEvent(Base):
    __tablename__ = "device_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sequence = Column(Integer)
    payload = Column(JSON)