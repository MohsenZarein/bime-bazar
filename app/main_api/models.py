from django.db import models
from django.contrib.auth import settings


class Insurance(models.Model):
    name = models.CharField(max_length=125)
    
    def __str__(self):
        return self.name
    


class Coupon(models.Model):
    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        related_name='coupons'
    )
    amount = models.PositiveIntegerField()
    probability = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.insurance.name + ' / ' + str(self.amount) + 'T'



class UserCoupon(models.Model):
    """
    Note :
        Used insurance & amount field instead 
        of forigen key to Coupon , just in case
        that if coupon object was deleted or changed,
        we still got the original data about coupon 
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='insurance_coupons'
    )
    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        related_name='user_coupons'
    )
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ':' + self.insurance.name
    

    class Meta:
        unique_together = (('user','insurance'),)

    