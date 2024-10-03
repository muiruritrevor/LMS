from django.contrib import admin
from .models import Book, Transaction

# Inline Configuration for Transactions
class TransactionInline(admin.TabularInline):
    """
    Defines an inline view of Transaction model within the Book admin interface.
    This allows viewing and editing related transactions directly in the Book detail page.
    """
    model = Transaction
    extra = 0  # Number of empty transaction forms to display (0 means no extra empty forms)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Book model.
    Configures display options, filtering, searching, and layout of the book management interface.
    """
    # Configure which fields appear in the books list
    list_display = ('title', 'author', 'isbn', 'status', 'total_copies', 'available_copies')
    
    # Add filter sidebar for refining book list by status and author
    list_filter = ('status', 'author')
    
    # Enable search functionality for title, author, and ISBN
    search_fields = ('title', 'author', 'isbn')
    
    # Include related transactions inline within book detail view
    inlines = [TransactionInline]
    
    # Organize book fields into logical sections using fieldsets
    fieldsets = (
        # Main book information section
        (None, {
            'fields': ('title', 'author', 'isbn', 'publish_date', 'status')
        }),
        # Inventory section
        ('Copies', {
            'fields': ('total_copies', 'available_copies')
        }),
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Transaction model.
    Configures display options, filtering, searching, and layout of the transaction management interface.
    """
    # Configure which fields appear in the transactions list
    list_display = ('user', 'book', 'checkout_date', 'due_date', 'return_date', 'is_overdue')
    
    # Add filter sidebar for refining transaction list by dates
    list_filter = ('due_date', 'return_date')
    
    # Enable search functionality for user and book
    search_fields = ('user__username', 'book__title')  # Allows searching related User and Book models
    
    # Organize transaction fields into logical sections
    fieldsets = (
        # Main transaction information
        (None, {
            'fields': ('user', 'book')
        }),
        # Date information section
        ('Dates', {
            'fields': ('checkout_date', 'due_date', 'return_date')
        }),
    )
