from pydantic import BaseModel
from typing import Optional

class DeviceEventCreate(BaseModel):
    device_id: str
    event_type: str
    uptime: Optional[float] = None
    traffic: Optional[float] = None
