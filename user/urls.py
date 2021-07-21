from django.urls import path
from .api import CreateUserAPI, UserAPI, LoginAPI

from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

app_name = 'user'


urlpatterns = [
    path(
        'create-user',
        CreateUserAPI.as_view(),
        name='create_user'
    ),
    path(
        'user',
        UserAPI.as_view(),
        name='user'
    ),
    path(
        'token/',
        TokenObtainSlidingView.as_view(),
        name='token_obtain'
    ),
    path(
        'token/refresh',
        TokenRefreshSlidingView.as_view(),
        name='token_refresh'
    ),
    path(
        'login',
        LoginAPI.as_view(),
        name='login'
    ),
]
