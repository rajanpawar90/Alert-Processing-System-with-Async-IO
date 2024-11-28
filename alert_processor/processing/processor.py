from typing import Optional
from ..models.base import BaseAlert, AlertStatus
from ..storage.base import AlertStorage
from ..services.base import LogService, AnalyzerService

class AlertProcessor:
    def __init__(
        self,
        storage: AlertStorage,
        log_service: LogService,
        analyzer_service: AnalyzerService
    ):
        self.storage = storage
        self.log_service = log_service
        self.analyzer_service = analyzer_service

    async def process_alert(self, alert: BaseAlert) -> Optional[str]:
        try:
            alert.status = AlertStatus.FETCHING_LOGS
            self.storage.update_alert(alert)
            
            logs = await self.log_service.fetch_logs(
                getattr(alert, 'service', 'unknown'),
                alert.alert_time
            )
            
            alert.status = AlertStatus.ANALYZING
            self.storage.update_alert(alert)
            
            analysis = await self.analyzer_service.analyze(
                alert.to_dict(),
                logs
            )
            
            alert.status = AlertStatus.COMPLETED
            self.storage.update_alert(alert)
            
            return analysis
            
        except Exception as e:
            alert.status = AlertStatus.FAILED
            alert.error = str(e)
            self.storage.update_alert(alert)
            raise