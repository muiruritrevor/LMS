from django.db import models
from accounts.models import User
from datetime import timedelta, date

# Book Model
class Book(models.Model):
    """
    Book model for storing book information.

    :Attr title: The title of the book
    :Attr author: The author of the book
    :Attr ISNB: The unique ISBN number of the book
    :Attr published_date: The published date of the book
    :Attr total_copies: The total number of copies
    :Attr available_copies: The number of available copies
    :Attr status: The availability status of the book


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