from rest_framework import serializers
from .models import UserCoupon, Insurance
from datetime import datetime


class InsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insurance
        fields = ('name',)


class UserCouponSerializer(serializers.ModelSerializer):
    insurance = InsuranceSerializer()

    class Meta:
        model = UserCoupon
        fields = ('__all__')


class DateSerializer(serializers.Serializer):
    year = serializers.IntegerField(required=False)
    month = serializers.IntegerField(required=False)
    day = serializers.IntegerField(required=False)
    hour = serializers.IntegerField(required=False)

    def validate_year(self, value):

        if value >= 1973 and value <= datetime.now().year:
            return value
        
        raise serializers.ValidationError('year is not proper')

    def validate_month(self, value):
        
        if value >= 1 and value <=12:
            return value
        
        raise serializers.ValidationError('month is not proper')

    def validate_day(self, value):

        if value >= 1 and value <=31:
            return value
        
        raise serializers.ValidationError('day is not proper')

    def validate_hour(self, value):

        if value >= 1 and value <=24:
            return value
        
        raise serializers.ValidationError('hour is not proper')



