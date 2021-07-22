from django.urls import path
from .api import GetRandomCouponAPI

app_name = 'main-api'

urlpatterns = [
    path(
        'get-random-coupon/<int:pk>',
        GetRandomCouponAPI.as_view(),
        name='get-random-coupon'
    ),
]
