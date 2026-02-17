from sqlalchemy import Column, Integer, DateTime
from app.core.database import Base

class NetworkMetric(Base):
    __tablename__ = "network_metrics"

    id = Column(Integer, primary_key=True, index=True)
    measure_time = Column(DateTime)

    total_devices = Column(Integer)
    active_devices = Column(Integer)

    data_sent = Column(Integer)
    data_received = Column(Integer)

    arp_requests = Column(Integer)
    tcp_packets = Column(Integer)
    udp_packets = Column(Integer)
    icmp_packets = Column(Integer)

    total_packets = Column(Integer)
