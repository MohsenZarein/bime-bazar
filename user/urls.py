from django.urls import path
from .api import CreateUserAPI, UserAPI

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
    )
]
