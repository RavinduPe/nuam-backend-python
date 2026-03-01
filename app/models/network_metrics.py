from sqlalchemy import Column, Integer, DateTime, BigInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class NetworkMetric(Base):
    __tablename__ = "network_metrics"

    id = Column(Integer, primary_key=True, index=True)
    measure_time = Column(DateTime)

    total_devices = Column(Integer)
    active_devices = Column(Integer)

    data_sent = Column(BigInteger)  # bytes
    data_received = Column(BigInteger)  # bytes

    arp_requests = Column(Integer)
    tcp_packets = Column(Integer)
    udp_packets = Column(Integer)
    icmp_packets = Column(Integer)

    total_packets = Column(Integer)


class DeviceMetric(Base):
    __tablename__ = "device_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    measure_time = Column(DateTime)
    
    # Topology data fields
    data_sent = Column(BigInteger, default=0)
    data_received = Column(BigInteger, default=0)
    packet_count = Column(Integer, default=0)
    status = Column(String)           # 'active', 'idle', etc.
    online = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    hostname = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    device_type = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    os = Column(String, nullable=True)
    
    device = relationship("Device")