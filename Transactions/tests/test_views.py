from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from Categories.models import Category
from ..models import Transaction, TransactionType, TransactionStatus
from Users.tests.utils.tokens import get_tokens_for_user
from django.urls import reverse
from rest_framework import status


class TransactionTests(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.category = Category.objects.create(name='mycategory', owner=self.user)
        self.category.save()

        self.transaction = Transaction.objects.create(
            title = 'transaction',
            amount = 1.00,
            currency = 'USD',
            user = self.user,
            category = self.category,
            type = 'Payment',
            status = 'Completed'
        )

    def authenticate(self):
        token = get_tokens_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_transaction_create_success(self):
        self.authenticate()

        response = self.client.post(
            reverse('transaction-list'),
            {
                'title': 'title',
                'amount': '68.99',
                'currency': 'EUR',
                'category': self.category.id,
                'type': 'Payment',
                'status': 'Completed'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('currency', response.data)
        self.assertIn('category', response.data)
        self.assertIn('type', response.data)
        self.assertIn('status', response.data)

    def test_transaction_create_failure(self):
        self.authenticate()
        response = self.client.post(reverse('transaction-list'), {'title': ''})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transaction_list(self):
        self.authenticate()
        response = self.client.get(reverse('transaction-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction(self):
        self.authenticate()
        response = self.client.get(reverse('transaction-detail', kwargs={'pk': self.transaction.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('currency', response.data)
        self.assertIn('category', response.data)
        self.assertIn('type', response.data)
        self.assertIn('status', response.data)

    def test_transaction_update(self):
        self.authenticate()

        response = self.client.put(
            reverse('transaction-detail', kwargs={'pk': self.transaction.id}),
            {
                'title': 'transaction',
                'amount': '5.00',
                'currency': 'USD',
                'category': self.category.id,
                'type': 'Payment',
                'status': 'Completed'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('currency', response.data)
        self.assertIn('category', response.data)
        self.assertIn('type', response.data)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['amount'], '5.00')

        self.transaction.refresh_from_db()

    def test_transaction_delete(self):
        self.authenticate()
        response = self.client.delete(reverse('transaction-detail', kwargs={'pk': self.transaction.id}))

        self.assertEqual(response.data, None)
