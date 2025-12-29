from datetime import datetime

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("SimpleMiddleware: Before the view")
        response = self.get_response(request)
        print("SimpleMiddleware: After the view")
        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f'[{datetime.now()}] - User: {request.user.last_name} - Path: {request.path}')
        response = self.get_response(request)
        return response