from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("SimpleMiddleware: Before the view")
        response = self.get_response(request)
        logger.info("SimpleMiddleware: After the view")
        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f'[{datetime.today()}] - User: {request.user.last_name} - Path: {request.path}')
        response = self.get_response(request)
        return response