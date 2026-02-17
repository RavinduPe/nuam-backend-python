from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from app.core.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)  # MAC address
    hostname = Column(String)
    ip_address = Column(String)
    device_type = Column(String)
    os = Column(String)
    vendor = Column(String)

    first_seen = Column(DateTime)
    last_seen = Column(DateTime)

    status = Column(String)  # ACTIVE / INACTIVE

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
