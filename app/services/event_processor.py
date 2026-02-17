import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.device_event import DeviceEvent
from app.models.network_metrics import NetworkMetric

from datetime import datetime, timedelta
from sqlalchemy import func

class EventProcessor:

    def __init__(self, db: Session):
        self.db = db

    def process_event(self, message: dict):

        event_type = message.get("type")
        subtype = message.get("subtype")
        payload = message.get("payload")

        # 1️⃣ DEVICE JOINED
        if subtype == "DEVICE_JOINED":
            self.handle_device_joined(payload)

        # 2️⃣ DEVICE IDLE
        elif subtype == "DEVICE_IDLE":
            self.handle_device_idle(payload)

        # 3️⃣ METRIC SNAPSHOT
        elif subtype == "PERIODIC_METRIC_STATE":
            self.handle_metric(payload)
            
    
    def handle_device_joined(self, payload):

        device_data = payload["device"]
        mac = device_data["device_id"]
        timestamp = datetime.fromisoformat(
            payload["timestamp"].replace("Z", "")
        )

        device = self.db.query(Device).filter(
            Device.device_id == mac
        ).first()

        if not device:
            device = Device(
                device_id=mac,
                hostname=device_data["hostname"],
                ip_address=device_data["ip_address"],
                device_type=device_data["device_type"],
                os=device_data["os"],
                vendor=device_data["vendor"],
                first_seen=timestamp,
                last_seen=timestamp,
                status="ACTIVE"
            )
            self.db.add(device)
        else:
            device.last_seen = timestamp
            device.status = "ACTIVE"

        # Save event history
        event = DeviceEvent(
            device_id=mac,
            event_type="DEVICE_JOINED",
            timestamp=timestamp,
            raw_json=json.dumps(payload)
        )
        self.db.add(event)

        self.db.commit()
        
    
    def handle_device_idle(self, payload):

        device_data = payload["device"]
        mac = device_data["device_id"]
        timestamp = datetime.fromisoformat(
            payload["timestamp"].replace("Z", "")
        )

        device = self.db.query(Device).filter(
            Device.device_id == mac
        ).first()

        if device:
            device.status = "INACTIVE"
            device.last_seen = timestamp

        event = DeviceEvent(
            device_id=mac,
            event_type="DEVICE_IDLE",
            timestamp=timestamp,
            raw_json=json.dumps(payload)
        )

        self.db.add(event)
        self.db.commit()
        
        
    def handle_metric(self, payload):

        metrics = payload["metrics"]

        metric_row = NetworkMetric(
            measure_time=datetime.fromisoformat(
                metrics["measure_time"].replace("Z", "")
            ),
            total_devices=metrics["total_devices"],
            active_devices=metrics["active_devices"],
            data_sent=metrics["data_sent"],
            data_received=metrics["data_received"],
            arp_requests=metrics["arp_requests"],
            tcp_packets=metrics["tcp_packets"],
            udp_packets=metrics["udp_packets"],
            icmp_packets=metrics["icmp_packets"],
            total_packets=metrics["total_packets"]
        )

        self.db.add(metric_row)
        self.db.commit()
        

    def get_dashboard_stats(self):

        today = datetime.utcnow().date()

        # New devices today
        new_devices_today = self.db.query(Device).filter(func.date(Device.first_seen) == today).count()

        # Inactive devices (time-based)
        threshold = datetime.utcnow() - timedelta(minutes=5)

        inactive_devices = self.db.query(Device).filter(Device.status=="INACTIVE").count()

        total_devices = self.db.query(Device).count()

        active_devices = self.db.query(Device).filter(Device.status=="ACTIVE").count()

        return {
            "new_devices_today": new_devices_today,
            "inactive_devices": inactive_devices,
            "active_devices": active_devices,
            "total_devices": total_devices
        }
        
    def sync_devices_from_engine(self, active_device_ids: list):
        for mac in active_device_ids:
            device = self.db.query(Device).filter(Device.device_id == mac).first()
            if not device:
                new_device = Device(
                    device_id=mac,
                    first_seen=datetime.utcnow(),
                    last_seen=datetime.utcnow(),
                    status="ACTIVE"
                )
                self.db.add(new_device)
        self.db.commit()




            
            
    

