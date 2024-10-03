from django.db import models
from accounts.models import User
from datetime import timedelta, date


class Book(models.Model):
    """
    Represents a book in the library system.

    Attributes:
        title (str): The title of the book (max 255 characters)
        author (str): The author's name (max 255 characters)
        isbn (str): Unique 13-digit ISBN identifier
        publish_date (date): The book's publication date
        total_copies (int): Total number of copies owned by the library
        available_copies (int): Current number of copies available for checkout
        status (str): Current availability status of the book
    """

    STATUS_CHOICES = [
        ('A', 'Available'),
        ('M', 'Maintenance'),
        ('R', 'Reserved'),
        ('C', 'Checked Out'),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publish_date = models.DateField()
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A',
        help_text='Book availability',
        )

    class Meta:
        ordering = ['available_copies']

    def __str__(self):
        return f"{self.title} by {self.author}"
     
class Transaction(models.Model):
    """
    Transaction Model to track the checkout and return of books.

    :Attr Transaction_TYPE: The type of transaction
    :Attr user: The user who checked out the book
    :Attr book: The book being checked out or returned
    :Attr checkout_date: The date the book was checked out
    :Attr due_date: The due date for returning the book
    :Attr return_date: The date the book was returned
    :Attr is_overdue: A flag to indicate if the book is overdue
    """

    Transaction_TYPE = [
        ('CO', 'Check Out'),
        ('RE', 'Return'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=date.today() + timedelta(days=14))  # 14-day borrow period
    return_date = models.DateField(null=True, blank=True)
    is_overdue = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['checkout_date']

    def __str__(self):
        return f"{self.user} checked out {self.book}"