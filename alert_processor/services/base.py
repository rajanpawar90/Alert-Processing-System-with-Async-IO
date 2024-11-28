from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime

class LogService(ABC):
    @abstractmethod
    async def fetch_logs(self, service: str, timestamp: datetime, **kwargs) -> List[Dict[str, Any]]:
        pass

class AnalyzerService(ABC):
    @abstractmethod
    async def analyze(self, alert_data: Dict[str, Any], logs: List[Dict[str, Any]]) -> str:
        pass