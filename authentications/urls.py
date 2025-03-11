from django.urls import path

from authentications.views import cookie_token_obtain_pair_view, cookie_token_refresh_view, cookie_token_logout_view, \
    protected_view, me_view

app_name = "authentications"

urlpatterns = [
    path('token/', cookie_token_obtain_pair_view, name='cookie_token_obtain_pair_view'),
    path('token/refresh/', cookie_token_refresh_view, name='cookie_token_refresh_view'),
    path('token/logout/', cookie_token_logout_view, name='cookie_token_logout_view'),
    path('token/protected/', protected_view, name='protected_view'),
    path('token/me/', me_view, name='me_view'),
]