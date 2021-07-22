from django.urls import path
from .api import GetRandomCouponAPI, GetInsuranceCouponInfoAPI

app_name = 'main-api'

urlpatterns = [
    path(
        'get-random-coupon/<int:pk>',
        GetRandomCouponAPI.as_view(),
        name='get-random-coupon'
    ),
    path(
        'get-insurance-coupon-info/<int:pk>',
        GetInsuranceCouponInfoAPI.as_view(),
        name='get-insurance-coupon-info'
    ),
]
