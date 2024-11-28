import threading
from typing import Dict, Optional
from .base import AlertStorage
from ..models.base import BaseAlert

class InMemoryAlertStorage(AlertStorage):
    def __init__(self):
        self._alerts: Dict[str, BaseAlert] = {}
        self._lock = threading.Lock()

    def add_alert(self, alert: BaseAlert) -> None:
        with self._lock:
            self._alerts[alert.id] = alert

    def get_alert(self, alert_id: str) -> Optional[BaseAlert]:
        with self._lock:
            return self._alerts.get(alert_id)

    def update_alert(self, alert: BaseAlert) -> None:
        with self._lock:
            if alert.id in self._alerts:
                self._alerts[alert.id] = alert