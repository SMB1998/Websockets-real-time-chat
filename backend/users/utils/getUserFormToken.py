from functools import wraps
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

User = get_user_model()

def get_user_from_token(request):
    try:
        # Authenticate the request to get a tuple of (user, token)
        user = JWTAuthentication().authenticate(request)[0]
        
        # Return the user if authentication is successful
        if user is not None:
            return user
        else:
            raise AuthenticationFailed('Usuario no encontrado')
    
    except InvalidToken:
        raise AuthenticationFailed('Token JWT inválido')
    except AuthenticationFailed:
        raise AuthenticationFailed('Autenticación fallida')