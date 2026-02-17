from datetime import datetime
from sqlalchemy import func
from app.models.device import Device
from app.models.network_metrics import NetworkMetric
import pandas as pd
import os

class ReportService:
    def __init__(self, db):
        self.db = db

    def generate_daily_report(self, report_date: datetime.date = None):
        if not report_date:
            report_date = datetime.utcnow().date()

        # Device stats
        total_devices = self.db.query(Device).count()
        new_devices = self.db.query(Device).filter(
            func.date(Device.first_seen) == report_date
        ).count()
        active_devices = self.db.query(Device).filter(Device.status == "ACTIVE").count()
        inactive_devices = self.db.query(Device).filter(Device.status == "INACTIVE").count()

        # Network metrics
        metrics = self.db.query(
            func.sum(NetworkMetric.data_sent),
            func.sum(NetworkMetric.data_received),
            func.sum(NetworkMetric.total_packets)
        ).filter(func.date(NetworkMetric.measure_time) == report_date).first()

        report = {
            "Date": str(report_date),
            "Total Devices": total_devices,
            "New Devices": new_devices,
            "Active Devices": active_devices,
            "Inactive Devices": inactive_devices,
            "Data Sent (bytes)": metrics[0] or 0,
            "Data Received (bytes)": metrics[1] or 0,
            "Total Packets": metrics[2] or 0
        }

        return report

    def save_report_excel(self, report: dict, folder: str = "reports/daily"):
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"daily_report_{report['Date']}.xlsx")
        df = pd.DataFrame([report])
        df.to_excel(filename, index=False)
        return filename
