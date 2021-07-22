from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from main_api.models import Insurance, Coupon, UserCoupon
from datetime import datetime
from django.db.models import Sum



def create_insurance(**params):
    """ helper function to create an insurance
        instance to avoid repeating code
    """
    return Insurance.objects.create(**params)




class PublicGetInsuranceCouponInfoAPITests(TestCase):
    """ Test the publicly available insurance coupon info API """
    
    def setUp(self):
        self.client = APIClient()
    

    def test_authentication_required(self):
        """ Test that authentication is required to access the endpoint """
        now = datetime.now()
        payload = {
            "year":now.year,
            "month":now.month,
            "day":now.day,
            "hour":now.hour
        }
        insurance = create_insurance(name='third-party')
        url = reverse('main-api:get-insurance-coupon-info', args=[insurance.pk,])
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateGetInsuranceCouponInfoAPITests(TestCase):
    """ Test the authorized user get insurance coupon info API """

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username='test',
            password='123456'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_unauthorized_user_accsess_fail(self):
        """ test that only superusers can access to the endpoint """
        user = get_user_model().objects.create_user(
            username='user',
            password='123456'
        )
        client = APIClient()
        client.force_authenticate(user=user)

        now = datetime.now()
        payload = {
            "year":now.year,
            "month":now.month,
            "day":now.day,
            "hour":now.hour
        }

        insurance = create_insurance(name='third-party')
        url = reverse('main-api:get-insurance-coupon-info', args=[insurance.pk])
        response = client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_get_insurance_coupon_info_success(self):
        """ test getting insurance coupon info successfuly """
        
        user1 = get_user_model().objects.create_user(
            username='user1',
            password='123456'
        )
        user2 = get_user_model().objects.create_user(
            username='user2',
            password='123456'
        )
        user3 = get_user_model().objects.create_user(
            username='user3',
            password='123456'
        )
        insurance = create_insurance(name='third-party')
        # create some coupons for users in db
        UserCoupon.objects.bulk_create([
            UserCoupon(insurance=insurance, amount=100000, user=user1),
            UserCoupon(insurance=insurance, amount=100000, user=user2),
            UserCoupon(insurance=insurance, amount=100000, user=user3),
        ])

        now = datetime.now()
        payload = {
            "year":now.year,
            "month":now.month,
            "day":now.day,
            "hour":now.hour
        }

        url = reverse('main-api:get-insurance-coupon-info', args=[insurance.pk])

        response = self.client.post(url, payload)

        obj = UserCoupon.objects.filter(insurance=insurance).aggregate(sum=Sum('amount'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(obj['sum']), str(response.data['sum']))
    

    def test_get_insurance_coupon_info_invalid_payload(self):
        """ test the endpoint with invalid date format as payload """
        now = datetime.now()
        payload = {
            "year":now.year + 1,
            "month":15 ,
            "day":40,
            "hour":25
        }
        insurance = create_insurance(name='third-party')
        url = reverse('main-api:get-insurance-coupon-info', args=[insurance.pk])

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


 
    def test_get_insurance_coupon_info_invalid_insurance(self):
        """ 
            test that making request to get insurance coupon info  
            with invalid insurance id (invalid url) will raise
            http 404 error
        """
        # clearly there is no insurance with id of 1 in db
        # cause we did not create any insurance instance before
        url = reverse('main-api:get-insurance-coupon-info', args=[1,])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




