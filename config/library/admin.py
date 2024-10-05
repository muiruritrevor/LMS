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
    list_display = [
        'user', 'book', 'checkout_date', 'due_date', 
        'return_date',  'penalty_amount', 'penalty_paid'
    ]
    list_filter = ['penalty_paid', 'transaction_type']
    search_fields = ['user__username', 'book__title']
    
    readonly_fields = ['penalty_amount', 'penalty_paid']
    
    actions = ['mark_penalties_paid']
    
    def mark_penalties_paid(self, request, queryset):
        updated = queryset.filter(penalty_amount__gt=0).update(penalty_paid=True)
        self.message_user(request, f'{updated} penalties marked as paid.')
    mark_penalties_paid.short_description = "Mark selected penalties as paid"

