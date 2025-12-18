from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .utils.tokens import get_tokens_for_user
# Create your tests here.


class UserTests(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)


    def authenticate(self):
        token = get_tokens_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_login_success(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_success(self):
        response = self.client.post(reverse('user_create'), {'username': 'username', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_failure(self):
        response = self.client.post(reverse('user_create'), {'testuser': 'username', 'testpassword': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile(self):
        self.authenticate()
        response = self.client.get(reverse('user_profile'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('username', response.data)

    def test_user_profile_failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer notuseraccesstoken')
        response = self.client.get(reverse('user_profile'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update(self):
        self.authenticate()
        payload = {'username': 'username', 'first_name': 'frst_name', 'last_name': 'lst_name'}
        response = self.client.put(reverse('user_profile_update'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)

    def test_user_password_update(self):
        self.user.refresh_from_db()
        self.authenticate()

        payload = {'old_password': self.password, 'new_password': 'newtestpassword'}
        response = self.client.put(reverse('user_password_update'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword'))

    def test_delete_user_success(self):
        self.authenticate()
        response = self.client.delete(reverse('user_delete'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(username=self.username).exists())

    def test_delete_user_unauthenticated(self):
        response = self.client.delete(reverse('user_delete'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
