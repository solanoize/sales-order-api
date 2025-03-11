from datetime import timedelta

from django.contrib.auth import authenticate
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from user_agents import parse

from authentications.serializers import LoginSerializer

def get_device_info(request):
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    user_agent_parsed = parse(user_agent)
    device = f"{user_agent_parsed.browser.family} - {user_agent_parsed.os.family}"
    ip_address = get_client_ip(request)
    return device, ip_address

def get_client_ip(request):
    """Mengambil IP address user dari request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

@csrf_exempt
@api_view(['POST'])
# @permission_classes([AllowAny])
def cookie_token_obtain_pair_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.data.get('username'),
                            password=serializer.data.get('password'))
        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"detail": "Login successfull"}, status=status.HTTP_200_OK)

            # Set cookie
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=str(refresh.access_token),
                # max_age=timedelta(minutes=20).total_seconds(),
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            # response.set_cookie(
            #     key="sessionID",
            #     value="331",
            #     # max_age=timedelta(minutes=20).total_seconds(),
            #     secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            #     # httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            #     samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            # )
            #
            # response.set_cookie(
            #     key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            #     value=str(refresh),
            #     # max_age=timedelta(minutes=20).total_seconds(),
            #     secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            #     httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            #     samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            # )

            return response

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def cookie_token_refresh_view(request):
    refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])

    if not refresh_token:
        return Response({"detail": "Refresh token not found"}, status=status.HTTP_403_FORBIDDEN)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=str(access_token),
            expires=timedelta(minutes=5),
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        return response
    except Exception:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def cookie_token_logout_view(request):
    response = Response({"detail": "Logged out"})
    response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
    response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
    return response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
    print("TOKEN COOKIE", token)
    decoded_token = AccessToken(token)  # Decode token
    print(get_client_ip(request))
    print(get_device_info(request))
    return Response({"detail": "You are authenticated"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response({"detail": "You are authenticated!"})


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})