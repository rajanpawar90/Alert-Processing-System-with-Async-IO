from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class AlertStatus(Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    FETCHING_LOGS = "fetching_logs"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Alert:
    id: str
    service: str
    environment: str
    message: str
    alert_time: datetime
    status: AlertStatus = AlertStatus.RECEIVED
    error: Optional[str] = None