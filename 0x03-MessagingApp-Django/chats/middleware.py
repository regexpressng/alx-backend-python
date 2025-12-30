
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        logger.info("SimpleMiddleware: Before the view")
        ip = request.user.role
        print(f"Request IP: {ip}")
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
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if 9 <= current_hour < 23:
            return self.get_response(request)
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access is restricted to business hours (9 AM to 5 PM).")
        

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_role = request.user.role.lower()
        if user_role == 'admin' or user_role == 'moderator':
            return self.get_response(request)
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You do not have permission to access this resource.")