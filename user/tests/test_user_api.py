from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse



CREATE_USER_URL = reverse('user:create_user')
USER_URL = reverse('user:user')
CREATE_TOKEN_SLIDING = reverse('user:token_obtain')
CREATE_TOKEN_REFRESH = reverse('user:token_refresh')


def create_user(**params):
    return get_user_model().objects.create_user(**params)



class PublicUserAPITest(TestCase):
    """ Test API requests that do not require authentication (Public API endpoints) """

    def setUp(self):
        self.client = APIClient()


    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        payload = {
            'username':'test',
            'password':'123456'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)


    def test_user_exists(self):
        """ Test creating a user that already exists fails """
        payload = {
            'username':'test',
            'password':'123456'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters """
        payload = {
            'username':'test',
            'password':'123'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(username=payload['username']).exists()
        self.assertFalse(user_exists)
    
    
    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        response = self.client.get(USER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

    def test_create_token_for_user(self):
        """ Test that a token is created for the user """
        payload = {
            'username':'test',
            'password':'123456'
        }
        create_user(**payload)
        response = self.client.post(CREATE_TOKEN_SLIDING, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given """
        create_user(username='test', password='123456')
        payload = {
            'username':'test',
            'password':'wrong'
        }
        response = self.client.post(CREATE_TOKEN_SLIDING, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_token_no_user(self):
        """ Test that token is not created if user does not exist """
        payload = {
            'user':'test',
            'password':'123456'
        }
        response = self.client.post(CREATE_TOKEN_SLIDING, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_token_missing_field(self):
        """ Test that token is not created if missing any field (username and password are required) """
        payload = {
            'username':'test',
            'password':''
        }
        response = self.client.post(CREATE_TOKEN_SLIDING, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    




class PrivateUserAPITest(TestCase):
    """ Test API requests that require authentication (Private API endpoints) """

    def setUp(self):
        self.user = create_user(
            username='test',
            password='123456'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """
        response = self.client.get(USER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'username':self.user.username,
            'id':self.user.id,
            'first_name':self.user.first_name,
            'last_name':self.user.last_name,
            'email':self.user.email
        })

    
    def test_post_me_not_allowed(self):
        """ Test that POST request to ME_URL is not allowed """
        response = self.client.post(USER_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)




