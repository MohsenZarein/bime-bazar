from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Insurance, Coupon, UserCoupon
from .serializers import UserCouponSerializer
from django.http import Http404
import random


class GetRandomCouponAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):

        try:
            return Insurance.objects.get(pk=pk)
        except Insurance.DoesNotExist:
            raise Http404


    def post(self, request, pk):

        insurance = self.get_object(pk)
        previous_coupon = None

        try:
            previous_coupon = UserCoupon.objects.select_related('insurance').get(insurance=insurance,user=self.request.user)
        except UserCoupon.DoesNotExist:
            pass

        if previous_coupon:
            serialized_coupon = UserCouponSerializer(previous_coupon)
            context = {
                'massage':f'You have requested coupon for {previous_coupon.insurance.name} before',
                'previous_coupon':serialized_coupon.data
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        coupons = Coupon.objects.filter(insurance=insurance)
        randnum = random.randrange(101)
        cumulative_probability = 0
        obj = None
        for c in coupons:
            if randnum in range(cumulative_probability,cumulative_probability + c.probability + 1):
                obj = UserCoupon(
                    insurance=insurance,
                    amount=c.amount,
                    user=self.request.user
                )
                obj.save()
                break

            cumulative_probability += c.probability
        
        if obj:
            serialized_coupon = UserCouponSerializer(obj)
            context = {
                'coupon':serialized_coupon.data
            }
            return Response(context)
        
        context = {
            'massage':'Could not find any coupon'
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)




