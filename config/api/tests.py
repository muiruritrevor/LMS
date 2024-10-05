# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import User, Book, Transaction

class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            publish_date='2023-01-01',
            total_copies=1,
            available_copies=1
        )

    def test_days_overdue_calculation(self):
        transaction = Transaction.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now().date() - timedelta(days=5)
        )
        self.assertEqual(transaction.days_overdue, 5)

    def test_penalty_calculation(self):
        transaction = Transaction.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now().date() - timedelta(days=10)
        )
        self.assertEqual(transaction.calculate_penalty(), Decimal('10.00'))

    def test_max_penalty(self):
        transaction = Transaction.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now().date() - timedelta(days=30)
        )
        self.assertEqual(transaction.calculate_penalty(), Transaction.MAX_PENALTY)

class TransactionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            publish_date='2023-01-01',
            total_copies=1,
            available_copies=1
        )
        
        self.transaction = Transaction.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now().date() - timedelta(days=5)
        )
        self.transaction.apply_penalty()

    def test_get_unpaid_penalties(self):
        url = reverse('transaction-unpaid-penalties')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['penalties']), 1)
        self.assertEqual(response.data['total_amount'], '5.00')

    def test_pay_penalty(self):
        url = reverse('transaction-pay-penalty', kwargs={'pk': self.transaction.pk})
        data = {'payment_method': 'credit_card'}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertTrue(self.transaction.penalty_paid)

    def test_pay_already_paid_penalty(self):
        self.transaction.penalty_paid = True
        self.transaction.save()
        
        url = reverse('transaction-pay-penalty', kwargs={'pk': self.transaction.pk})
        data = {'payment_method': 'credit_card'}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def run_tests():
    # This function is for demonstration purposes
    import unittest
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TransactionModelTests)
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TransactionAPITests))
    unittest.TextTestRunner().run(test_suite)