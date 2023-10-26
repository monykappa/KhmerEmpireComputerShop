    
class RewriteURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Rewrite the URL to '/home' for all requests
        request.path = '/home'
        return self.get_response(request)
