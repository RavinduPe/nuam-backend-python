from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating a new device event
class DeviceEventCreate(BaseModel):
    device_id: str
    event_type: str

# Schema for returning device event (includes ID and timestamp)
class DeviceEventResponse(BaseModel):
    id: int
    device_id: str
    event_type: str
    timestamp: datetime

    class Config:
        orm_mode = True
