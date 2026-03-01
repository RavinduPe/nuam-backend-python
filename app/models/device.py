from sqlalchemy import Column, String, DateTime, Integer, Boolean, BigInteger
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

    status = Column(String)  # ACTIVE / INACTIVE / IDLE
    online = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    
    # Traffic data
    data_sent = Column(BigInteger, default=0)  # bytes
    data_received = Column(BigInteger, default=0)  # bytes
    packet_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())