from abc import ABC, abstractmethod
from typing import Optional
from ..models.base import BaseAlert

class AlertStorage(ABC):
    @abstractmethod
    def add_alert(self, alert: BaseAlert) -> None:
        pass

    @abstractmethod
    def get_alert(self, alert_id: str) -> Optional[BaseAlert]:
        pass

    @abstractmethod
    def update_alert(self, alert: BaseAlert) -> None:
        pass