from django.contrib import admin
from .models import Insurance, Coupon, UserCoupon

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id','insurance', 'amount', 'probability']
    list_select_related = ['insurance',]


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'insurance', 'amount', 'created']
    list_select_related = ['user', 'insurance',]