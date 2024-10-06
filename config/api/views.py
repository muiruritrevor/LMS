from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BookSerializer, TransactionSerializer, UserSerializer, ProfileSerializer
from library.models import Book, Transaction
from accounts.models import User, Profile

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Book model.
    
    This ViewSet provides list, create, retrieve, update, and delete actions for books.
    It also includes a custom action to list available books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom action to list all available books.
        
        This action filters books that are marked as available and have at least one copy available.
        """
        available_books = self.get_queryset().filter(status=Book.Status.AVAILABLE, available_copies__gt=0)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Transaction model.
    
    This ViewSet provides list, create, retrieve, update, and delete actions for transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay_penalty(self, request, pk=None):
        """Endpoint to pay penalty for a specific transaction."""
        transaction = self.get_object()
        serializer = PenaltyPaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if transaction.penalty_paid:
            return Response(
                {"error": "Penalty already paid"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if transaction.penalty_amount <= 0:
            return Response(
                {"error": "No penalty to pay"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        

        success = transaction.pay_penalty()
        
        if success:
            return Response({"status": "Penalty paid successfully"})
        return Response(
            {"error": "Failed to process payment"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def unpaid_penalties(self, request):
        """Get all unpaid penalties for the current user."""
        penalties = self.get_queryset().filter(
            penalty_paid=False,
            penalty_amount__gt=0
        )
        total_amount = penalties.aggregate(
            total=Sum('penalty_amount')
        )['total'] or 0
        
        serializer = self.get_serializer(penalties, many=True)
        return Response({
            'penalties': serializer.data,
            'total_amount': total_amount
        })

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on User model.
    
    This ViewSet provides list, create, retrieve, update, and delete actions for users.
    It uses different permission classes based on the action being performed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        
        'create' action is allowed for any user (AllowAny), while other actions require authentication.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Profile model.
    
    This ViewSet provides list, create, retrieve, update, and delete actions for user profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class CheckoutBookView(generics.CreateAPIView):
    """
    View for handling book checkout process.
    
    This view creates a new transaction for checking out a book.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests to checkout a book.
        
        This method attempts to checkout a book for the authenticated user.
        It creates a new transaction if the book is available.
        """

        all_books = Book.objects.values_list('id', flat=True)
        print("Available book IDs:", list(all_books))  # This line logs available IDs
        
        book_id = request.data.get('book')
        
        try:
            book = Book.objects.get(id=book_id)
            transaction = book.checkout(request.user)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(generics.UpdateAPIView):
    """
    View for handling book return process.
    
    This view updates an existing transaction to mark a book as returned.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Handle PUT/PATCH requests to return a book.
        
        This method attempts to return a book for the authenticated user.
        It updates the existing transaction and the book's availability.
        """
        transaction = self.get_object()
        try:
            transaction.book.return_book(request.user)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)