from aiohttp import web

from alert_processor.storage.memory import InMemoryAlertStorage
from alert_processor.services.elasticsearch import ElasticsearchLogService
from alert_processor.services.llm import LLMAnalyzerService
from alert_processor.processing.processor import AlertProcessor
from alert_processor.api.handlers import AlertHandler

async def init_app():
    # Initialize services
    storage = InMemoryAlertStorage()
    log_service = ElasticsearchLogService("http://elasticsearch:9200")
    analyzer_service = LLMAnalyzerService("http://llm-service/analyze")
    
    # Initialize processor
    processor = AlertProcessor(storage, log_service, analyzer_service)
    
    # Initialize API handlers
    alert_handler = AlertHandler(storage, processor)
    
    # Setup application and routes
    app = web.Application()
    app.router.add_post("/alerts", alert_handler.handle_alert)
    app.router.add_get("/alerts/{alert_id}/status", alert_handler.get_status)
    
    return app

if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host="0.0.0.0", port=8080)