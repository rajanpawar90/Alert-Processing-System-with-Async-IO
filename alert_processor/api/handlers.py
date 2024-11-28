from aiohttp import web
import asyncio
import uuid
from datetime import datetime
from typing import Dict

from ..models.base import ServiceAlert, AlertStatus
from ..storage.base import AlertStorage
from ..processing.processor import AlertProcessor

class AlertHandler:
    def __init__(self, storage: AlertStorage, processor: AlertProcessor):
        self.storage = storage
        self.processor = processor

    async def handle_alert(self, request: web.Request) -> web.Response:
        try:
            data = await request.json()
            alert_id = str(uuid.uuid4())
            
            alert = ServiceAlert(
                id=alert_id,
                service=data["service"],
                environment=data["environment"],
                message=data["message"],
                alert_time=datetime.fromisoformat(data["alert_time"])
            )
            
            self.storage.add_alert(alert)
            asyncio.create_task(self.processor.process_alert(alert))
            
            return web.json_response({
                "alert_id": alert_id,
                "status": "accepted"
            })
            
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)

    async def get_status(self, request: web.Request) -> web.Response:
        alert_id = request.match_info["alert_id"]
        alert = self.storage.get_alert(alert_id)
        
        if not alert:
            return web.json_response({"error": "Alert not found"}, status=404)
            
        return web.json_response(alert.to_dict())