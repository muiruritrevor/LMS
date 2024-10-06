from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import User, Book, Transaction

class PenaltySystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='p3JtF@example.com',
            first_name='Test',
            last_name='User',
            username='testuser',
            password='testpass'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            genre='Fiction',
            publish_date='2023-01-01',
            total_copies=1,
            available_copies=1
        )
        
    def test_overdue_calculation(self):
        # Create an overdue transaction
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
        
        # Assuming the penalty rate is $1 per day
        DAILY_PENALTY_RATE = Decimal('1.00')
        expected_penalty = min(Decimal('10.00'), Transaction.MAX_PENALTY)  # 10 days * $1/day
        
        self.assertEqual(transaction.calculate_penalty(), expected_penalty)
        
    def test_max_penalty(self):
        transaction = Transaction.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now().date() - timedelta(days=60)
        )
        
        self.assertEqual(
            transaction.calculate_penalty(),
            Transaction.MAX_PENALTY
        )
        
    def test_user_can_borrow_books(self):
        # Create multiple overdue transactions
        for _ in range(3):
            transaction = Transaction.objects.create(
                user=self.user,
                book=self.book,
                due_date=timezone.now().date() - timedelta(days=20)
            )
            transaction.apply_penalty()  # Assuming this method applies penalties
            
        self.assertFalse(self.user.can_borrow_books())
