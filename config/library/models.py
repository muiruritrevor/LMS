from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import User
from datetime import timedelta

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
    
        Returns:
            Transaction or None: The created transaction if successful, raises ValueError if the book is unavailable.
        """
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
            Transaction or None: The updated transaction if successful, None if not found
        """
        transaction = self.transaction_set.filter(
            user=user, 
            return_date__isnull=True
        ).first()
        
        if not transaction:
            raise ValueError("No active transaction found for this book and user")
        
        self.available_copies += 1
        self.save()
        
        transaction.return_book()
        return transaction


class Transaction(models.Model):
    """
    Tracks the checkout and return of books.
    """

    class TransactionType(models.TextChoices):
        CHECK_OUT = 'CO', 'Check Out'
        RETURN = 'RE', 'Return'

    LOAN_PERIOD_DAYS = 14

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=2,
        choices=TransactionType.choices,
        default=TransactionType.CHECK_OUT
    )
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-checkout_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['book']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        action = "returned" if self.return_date else "checked out"
        return f"{self.user} {action} {self.book}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now().date() + timedelta(days=self.LOAN_PERIOD_DAYS)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if the book is overdue."""
        if self.return_date:
            return False
        return timezone.now().date() > self.due_date

    def return_book(self):
        """Mark the transaction as returned."""
        self.return_date = timezone.now().date()
        self.transaction_type = self.TransactionType.RETURN
        self.save()

    @classmethod
    def get_active_transaction(cls, user, book):
        """Get an active transaction for a user and book."""
        return cls.objects.filter(
            user=user, 
            book=book, 
            return_date__isnull=True
        ).first()