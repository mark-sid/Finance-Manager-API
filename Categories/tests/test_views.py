from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Category
from Users.tests.utils.tokens import get_tokens_for_user
from django.urls import reverse
from rest_framework import status


class CategoryTests(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.category = Category.objects.create(name='mycategory', owner=self.user)
        self.category.save()

    def authenticate(self):
        token = get_tokens_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_category_create_success(self):
        self.authenticate()
        response = self.client.post(reverse('category-list'), {'name': 'mycategory'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('owner', response.data)


    def test_category_create_failure(self):
        self.authenticate()
        response = self.client.post(reverse('category-list'), {'name': ''})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_list(self):
        self.authenticate()
        response = self.client.get(reverse('category-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        self.authenticate()
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)


    def test_category_update(self):
        self.authenticate()
        response = self.client.put(
            reverse('category-detail', kwargs={'pk': self.category.id}),
            {'name': 'cat'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], 'cat')

        self.category.refresh_from_db()

    def test_category_delete(self):
        self.authenticate()
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category.id}))

        self.assertEqual(response.data, None)