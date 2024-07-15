from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Process request (e.g., logging)
        response = await call_next(request)
        # Process response (e.g., add headers)
        response.headers['X-Custom-Header'] = 'MyHeaderValue'
        return response
