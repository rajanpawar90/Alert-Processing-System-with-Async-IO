from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class AlertStatus(Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    FETCHING_LOGS = "fetching_logs"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class BaseAlert(ABC):
    id: str
    alert_time: datetime
    status: AlertStatus = AlertStatus.RECEIVED
    error: Optional[str] = None

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

@dataclass
class ServiceAlert(BaseAlert):
    service: str
    environment: str
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "service": self.service,
            "environment": self.environment,
            "message": self.message,
            "alert_time": self.alert_time.isoformat(),
            "status": self.status.value,
            "error": self.error
        }