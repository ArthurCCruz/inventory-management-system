# Create your views here.
from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer
from typing import TypedDict, cast

User = get_user_model()

REFRESH_COOKIE_NAME = "refresh_token"

def _set_refresh_cookie(response: Response, refresh: str):
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh,
        httponly=True,
        secure=True,        # True in production with HTTPS
        samesite="None",      # "None" (with secure=True) if truly cross-site
        path="/v1/auth/",   # cookie only sent to auth endpoints
        max_age=14 * 24 * 60 * 60,
    )

def _clear_refresh_cookie(response: Response):
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/v1/auth/", samesite="None")

class LoginData(TypedDict):
    username: str
    password: str

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = cast(LoginData, serializer.validated_data)
    
    user = authenticate(
        request,
        username=data["username"],
        password=data["password"],
    )

    if not user:
        return Response({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    resp = Response(
        {
            "access": access,
            "user": {"id": user.id, "username": user.username, "name": user.get_full_name()},
        },
        status=200,
    )
    _set_refresh_cookie(resp, str(refresh))
    return resp

@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_view(request):
    """
    Reads refresh token from HttpOnly cookie, returns new access token.
    """
    refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        return Response({"detail": "No refresh token cookie"}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        access = str(refresh.access_token)
        return Response({"access": access}, status=200)
    except TokenError:
        return Response({"detail": "Invalid refresh token"}, status=401)

@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    """
    Clears refresh cookie.
    """
    resp = Response({"detail": "Logged out"}, status=200)
    _clear_refresh_cookie(resp)
    return resp

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
	user = request.user
	return Response({"id": user.id, "username": user.username, "name": user.get_full_name()})