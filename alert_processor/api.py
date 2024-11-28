from aiohttp import web
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict

from .models import Alert, AlertStatus
from .state_manager import StateManager
from .log_fetcher import LogFetcher
from .llm_analyzer import LLMAnalyzer

class AlertAPI:
    def __init__(self):
        self.state_manager = StateManager()
        self.log_fetcher = LogFetcher("http://elasticsearch:9200")
        self.llm_analyzer = LLMAnalyzer("http://llm-service/analyze")
        
    async def process_alert(self, alert: Alert):
        try:
            self.state_manager.update_alert_status(alert.id, AlertStatus.FETCHING_LOGS)
            logs = await self.log_fetcher.fetch_logs(alert.service, alert.alert_time)
            
            self.state_manager.update_alert_status(alert.id, AlertStatus.ANALYZING)
            analysis = await self.llm_analyzer.analyze_logs(alert.__dict__, logs)
            
            self.state_manager.update_alert_status(alert.id, AlertStatus.COMPLETED)
            return analysis
            
        except Exception as e:
            self.state_manager.update_alert_status(alert.id, AlertStatus.FAILED, str(e))
            raise
    
    async def handle_alert(self, request: web.Request) -> web.Response:
        try:
            data = await request.json()
            alert_id = str(uuid.uuid4())
            
            alert = Alert(
                id=alert_id,
                service=data["service"],
                environment=data["environment"],
                message=data["message"],
                alert_time=datetime.fromisoformat(data["alert_time"])
            )
            
            self.state_manager.add_alert(alert)
            
            # Start processing in background
            asyncio.create_task(self.process_alert(alert))
            
            return web.json_response({"alert_id": alert_id, "status": "accepted"})
            
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
    
    async def get_status(self, request: web.Request) -> web.Response:
        alert_id = request.match_info["alert_id"]
        alert = self.state_manager.get_alert(alert_id)
        
        if not alert:
            return web.json_response({"error": "Alert not found"}, status=404)
            
        return web.json_response({
            "alert_id": alert.id,
            "status": alert.status.value,
            "error": alert.error
        })