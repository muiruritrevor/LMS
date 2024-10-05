from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import User
from datetime import timedelta
from decimal import Decimal

class Book(models.Model):
    """
    Represents a book in the library system.

    Attributes:
        title (str): The title of the book
        author (str): The author's name
        isbn (str): Unique 13-digit ISBN identifier
        publish_date (date): The book's publication date
        total_copies (int): Total number of copies owned by the library
        available_copies (int): Current number of copies available for checkout
        status (str): Current availability status of the book
    """

    class Status(models.TextChoices):
        AVAILABLE = 'A', 'Available'
        MAINTENANCE = 'M', 'Maintenance'
        RESERVED = 'R', 'Reserved'
        CHECKED_OUT = 'C', 'Checked Out'

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publish_date = models.DateField()
    genre = models.CharField(max_length=255, null=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def clean(self):
        """Validate the book's data ensuring that available copies do not exceed total copies."""
        if self.available_copies > self.total_copies:
            raise ValidationError("Available copies cannot exceed total copies")

    def save(self, *args, **kwargs):
        """Validate the book's data and update the book's status."""
        self.full_clean()
        self.update_status()
        super().save(*args, **kwargs) 

    def update_status(self):
        """Updates the status based on available copies."""
        if self.available_copies == 0:
            self.status = self.Status.CHECKED_OUT
        elif self.available_copies > 0:
            self.status = self.Status.AVAILABLE

    @property
    def is_available(self):
        """Check if the book is available for checkout."""
        return self.status == self.Status.AVAILABLE and self.available_copies > 0

    def checkout(self, user):
        """
        Attempt to checkout the book to a user.
        Added checking for unpaid penalties.
    
        Returns:
            Transaction or None: The created transaction if successful, raises ValueError if the book is unavailable.
        """

        if not user.can_borrow_books():
            raise ValueError("cannot checkout book because of unpaid penalties")

        # Check if the book is available using the `is_available` property
        if not self.is_available:
            raise ValueError("Book is not available for checkout")
    
        # Decrement available copies and save the book
        self.available_copies -= 1
        self.save()
    
        # Create a new transaction for checking out the book
        return Transaction.objects.create(
            user=user,
            book=self,
            transaction_type=Transaction.TransactionType.CHECK_OUT
        )


    def return_book(self, user):
        """
        Attempt to return the book from a user.
        
        Returns:
            transaction or ValueError: The updated transaction if successful, VealueError if not found
        """
        transaction = self.transaction_set.filter(
            user=user, 
            return_date__isnull=True
        ).first()
        
        if not transaction:
            raise ValueError("No active transaction found for this book and user")
        
        self.available_copies += 1
        self.save()
        
        transaction.return_date = timezone.now()
        transaction.save()
        return transaction


class Transaction(models.Model):
    """
    Tracks the checkout, return, and penalties for books.
    
    Constants:
        PENALTY_RATE: The daily rate for overdue books
        MAX_PENALTY: The maximum penalty amount per transaction
        LOAN_PERIOD_DAYS: The standard loan period
    """

    class TransactionType(models.TextChoices):
        CHECK_OUT = 'CO', 'Check Out'
        RETURN = 'RE', 'Return'
    # constants
    PENALTY_RATE = Decimal('2.00')
    MAX_PENALTY = Decimal('40.00')
    LOAN_PERIOD_DAYS = 90

    # Relationship fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # Transaction details
    transaction_type = models.CharField(
        max_length=2,
        choices=TransactionType.choices,
        default=TransactionType.CHECK_OUT
    )
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    # penalty fields
    penalty_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default= Decimal('0.00'),
    )
    
    penalty_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-checkout_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['book']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        status = "returned" if self.return_date else "checked out"
        penalty_status = f" (Penalty: ${self.penalty_amount})" if self.penalty_amount > 0 else ""
        return f"{self.user} {status} {self.book}{penalty_status}"

    @property
    def is_overdue(self):
        """Check if the book is overdue."""
        if self.return_date:
            return False
        return timezone.now().date() > self.due_date
    
    def calculate_penalty(self):
        """Calculate the penalty amount based on days overdue."""
        if not self.is_overdue:
            return Decimal('0.00')
        
        penalty = self.is_overdue * self.PENALTY_RATE
        return min(penalty, self.MAX_PENALTY)
    
    def apply_penalty(self):
        """Apply the penalty to the transaction."""
        self.penalty_amount = self.calculate_penalty()
        self.save()
    
    def pay_penalty(self):
        """Mark the penalty as paid."""
        if self.penalty_amount > 0:
            self.penalty_paid = True
            self.save()
    
    def return_book(self):
        """Mark the transaction as returned and apply penalty calculation if needed."""
        self.return_date = timezone.now().date()
        self.transaction_type = self.TransactionType.RETURN
        self.apply_penalty()
        self.save()

    def save(self, *args, **kwargs):
        """Override save to ensure due date is set."""
        if not self.due_date:
            self.due_date = timezone.now().date() + timedelta(days=self.LOAN_PERIOD_DAYS)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_transaction(cls, user, book):
        """Get an active transaction for a user and book."""
        return cls.objects.filter(
            user=user, 
            book=book, 
            return_date__isnull=True
        ).first()