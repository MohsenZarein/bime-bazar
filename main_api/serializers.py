from rest_framework import serializers
from .models import UserCoupon, Insurance


class InsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insurance
        fields = ('name',)


class UserCouponSerializer(serializers.ModelSerializer):
    insurance = InsuranceSerializer()

    class Meta:
        model = UserCoupon
        fields = ('__all__')
