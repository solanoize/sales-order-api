from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthenticationFromCookie(JWTAuthentication):
    def authenticate(self, request):
        # Ambil token dari cookie (misalnya cookie bernama "access_token")
        token = request.COOKIES.get("access_token")

        if token is None:
            return None  # Tidak ada token, lanjutkan ke autentikasi default

        # Verifikasi token
        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None  # Token tidak valid
