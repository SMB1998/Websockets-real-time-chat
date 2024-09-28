

from functools import wraps
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

User = get_user_model()

def get_user_from_token(request):
    try:
        user = JWTAuthentication().authenticate(request)[0]
        return user
    except InvalidToken:
        raise AuthenticationFailed('Token JWT inválido')
    except AuthenticationFailed:
        raise AuthenticationFailed('Autenticación fallida')