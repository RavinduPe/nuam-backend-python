import json
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.device import Device
from app.models.device_event import DeviceEvent
from app.models.network_metrics import NetworkMetric


class EventProcessor:

    def __init__(self, db: Session):
        self.db = db

    def process_event(self, message: dict):
        try:
            subtype = message.get("subtype")
            payload = message.get("payload")

            if subtype == "DEVICE_JOINED":
                self.handle_device_joined(payload)

            elif subtype == "DEVICE_IDLE":
                self.handle_device_idle(payload)

            elif subtype == "PERIODIC_METRIC_STATE":
                self.handle_metric(payload)

            elif subtype == "PERIODIC_TOPOLOGY_STATE":
                self.handle_topology_snapshot(payload)

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e

    def handle_device_joined(self, payload):
        device_data = payload["device"]
        mac = device_data["device_id"]

        timestamp = datetime.fromisoformat(
            payload["timestamp"].replace("Z", "+00:00")
        )

        device = self.db.query(Device).filter_by(device_id=mac).first()

        if not device:
            device = Device(
                device_id=mac,
                hostname=device_data.get("hostname"),
                ip_address=device_data.get("ip_address"),
                device_type=device_data.get("device_type"),
                os=device_data.get("os"),
                vendor=device_data.get("vendor"),
                first_seen=timestamp,
                last_seen=timestamp,
                status="ACTIVE"
            )
            self.db.add(device)
        else:
            device.last_seen = timestamp
            device.status = "ACTIVE"

        event = DeviceEvent(
            device_id=mac,
            event_type="DEVICE_JOINED",
            timestamp=timestamp,
            raw_json=json.dumps(payload)
        )

        self.db.add(event)
    def handle_device_idle(self, payload):
        device_data = payload["device"]
        mac = device_data["device_id"]

        timestamp = datetime.fromisoformat(
            payload["timestamp"].replace("Z", "+00:00")
        )

        device = self.db.query(Device).filter_by(device_id=mac).first()

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


    def handle_metric(self, payload):
        metrics = payload["metrics"]

        metric_row = NetworkMetric(
            measure_time=datetime.fromisoformat(
                metrics["measure_time"].replace("Z", "+00:00")
            ),
            total_devices=metrics.get("total_devices", 0),
            active_devices=metrics.get("active_devices", 0),
            data_sent=metrics.get("data_sent", 0),
            data_received=metrics.get("data_received", 0),
            arp_requests=metrics.get("arp_requests", 0),
            tcp_packets=metrics.get("tcp_packets", 0),
            udp_packets=metrics.get("udp_packets", 0),
            icmp_packets=metrics.get("icmp_packets", 0),
            total_packets=metrics.get("total_packets", 0)
        )

        self.db.add(metric_row)


    def get_dashboard_stats(self):
        today = datetime.now(timezone.utc).date()

        new_devices_today = self.db.query(Device).filter(
            func.date(Device.first_seen) == today
        ).count()

        inactive_devices = self.db.query(Device).filter_by(status="INACTIVE").count()
        active_devices = self.db.query(Device).filter_by(status="ACTIVE").count()
        total_devices = self.db.query(Device).count()

        return {
            "new_devices_today": new_devices_today,
            "inactive_devices": inactive_devices,
            "active_devices": active_devices,
            "total_devices": total_devices
        }



    def sync_devices_from_engine(self, active_device_ids: list):
        now = datetime.now(timezone.utc)

        for mac in active_device_ids:
            device = self.db.query(Device).filter_by(device_id=mac).first()
            if not device:
                new_device = Device(
                    device_id=mac,
                    first_seen=now,
                    last_seen=now,
                    status="ACTIVE"
                )
                self.db.add(new_device)

        self.db.commit()



    def handle_topology_snapshot(self, payload):
        devices = payload["topology"]["devices"]

        for device_data in devices:
            mac = device_data["mac"]

            device = self.db.query(Device).filter_by(device_id=mac).first()

            first_seen = device_data.get("first_seen")
            last_seen = device_data.get("last_seen")

            first_seen_dt = (
                datetime.fromisoformat(first_seen.replace("Z", "+00:00"))
                if first_seen else datetime.now(timezone.utc)
            )

            last_seen_dt = (
                datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
                if last_seen else datetime.now(timezone.utc)
            )

            if not device:
                device = Device(
                    device_id=mac,
                    hostname=device_data.get("hostname"),
                    ip_address=device_data.get("ip_address"),
                    device_type=device_data.get("device_type"),
                    os=device_data.get("os"),
                    vendor=device_data.get("vendor"),
                    first_seen=first_seen_dt,
                    last_seen=last_seen_dt,
                    status="ACTIVE" if device_data.get("online") else "INACTIVE"
                )
                self.db.add(device)
            else:
                device.hostname = device_data.get("hostname")
                device.ip_address = device_data.get("ip_address")
                device.os = device_data.get("os")
                device.vendor = device_data.get("vendor")
                device.last_seen = last_seen_dt
                device.status = "ACTIVE" if device_data.get("online") else "INACTIVE"