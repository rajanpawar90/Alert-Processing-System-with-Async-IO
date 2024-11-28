import threading
from typing import Dict
from .models import Alert, AlertStatus

class StateManager:
    def __init__(self):
        self._alerts: Dict[str, Alert] = {}
        self._lock = threading.Lock()
    
    def add_alert(self, alert: Alert) -> None:
        with self._lock:
            self._alerts[alert.id] = alert
    
    def update_alert_status(self, alert_id: str, status: AlertStatus, error: str = None) -> None:
        with self._lock:
            if alert_id in self._alerts:
                alert = self._alerts[alert_id]
                alert.status = status
                alert.error = error
    
    def get_alert(self, alert_id: str) -> Alert:
        with self._lock:
            return self._alerts.get(alert_id)