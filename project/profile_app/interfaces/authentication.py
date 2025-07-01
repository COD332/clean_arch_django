from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class CookieTokenAuthentication(TokenAuthentication):
    """
    Reads the DRF Token from an HTTP-only cookie named 'auth_token'.
    Falls back to the standard Authorization header if not found.
    """
    def authenticate(self, request):
        # Try cookie first
        token = request.COOKIES.get('auth_token')
        if token:
            # prefix like "Token <key>" is optional here; DRF's TokenAuthentication
            # will accept raw key if prefix is omitted.
            return self.authenticate_credentials(token)
        # Fallback to normal header behavior
        return super().authenticate(request)
