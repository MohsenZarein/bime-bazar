from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from main_api.models import Insurance, Coupon, UserCoupon



def create_insurance(**params):
    """ helper function to create an insurance
        instance to avoid repeating code
    """
    return Insurance.objects.create(**params)


def create_coupons(insurance):
    """ helper function to create coupon
        instances to avoid repeating code
    """
    Coupon.objects.bulk_create([
        Coupon(insurance=insurance, amount=100000, probability=40),
        Coupon(insurance=insurance, amount=150000, probability=25),
        Coupon(insurance=insurance, amount=200000, probability=20),
        Coupon(insurance=insurance, amount=250000, probability=15),
    ])




class PublicGetRandomCouponAPITests(TestCase):
    """ Test the publicly available random coupon API """
    
    def setUp(self):
        self.client = APIClient()
    

    def test_authentication_required(self):
        """ Test that authentication is required to access the endpoint """
        insurance = create_insurance(name='third-party')
        url = reverse('main-api:get-random-coupon', args=[insurance.pk,])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        



class PrivateGetRandomCouponAPITests(TestCase):
    """ Test the authorized user random coupon API """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123456'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    

    def test_get_random_coupon_successful(self):
        """ test getting a random coupon successfuly """
        insurance = create_insurance(name='third-party')
        create_coupons(insurance)
        url = reverse('main-api:get-random-coupon', args=[insurance.pk,])
        response = self.client.post(url)

        exists = UserCoupon.objects.filter(
            insurance=insurance,
            user=self.user
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(exists)
    

    def test_get_random_coupon_fails(self):
        """ 
            test that getting random coupon fails 
            if you have already recieved a coupon
            for that specific insurance
        """
        insurance = create_insurance(name='third-party')
        UserCoupon.objects.create(
            insurance=insurance,
            amount=100000,
            user=self.user
        )
        url = reverse('main-api:get-random-coupon', args=[insurance.pk,])
        response = self.client.post(url)

        count = UserCoupon.objects.filter(
            insurance=insurance,
            user=self.user
        ).count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count, 1)
        


    def test_get_random_coupon_invalid_insurance(self):
        """ 
            test that making request to get coupon with 
            invalid insurance id (invalid url) will raise
            http 404 error
        """
        # clearly there is no insurance with id of 1 in db
        # cause we did not create any insurance instance before
        url = reverse('main-api:get-random-coupon', args=[1,])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_get_random_coupon_while_not_exists_any_coupon(self):
        """
            test the endpoint for requesting a coupon while there is
            not any coupons or no coupons found with that random number 
            and exist probabilitis
        """
        insurance = create_insurance(name='third-party')
        url = reverse('main-api:get-random-coupon', args=[insurance.pk,])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


        


