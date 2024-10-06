from rest_framework import serializers
from library.models import Book, Transaction
from accounts.models import User, Profile


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Handles the serialization and deserialization of Book objects, including
    validation and creation/update operations.
    """
    
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "isbn",
            "genre",
            "publish_date",
            "total_copies",
            "available_copies",
            "status"
        ]
        
    def validate_isbn(self, value):
        """
        Validate the ISBN format.
        
        Args:
            value (str): The ISBN to validate
            
        Returns:
            str: The validated ISBN
            
        Raises:
            serializers.ValidationError: If ISBN format is invalid
        """

        if len(value) not in [13]:
            raise serializers.ValidationError("ISBN must be13 characters")
        return value
    
    def validate(self, data):
        """
        Validate the entire object.
        
        Ensures that available_copies doesn't exceed total_copies.
        
        Args:
            data (dict): The data to validate
            
        Returns:
            dict: The validated data
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if data.get('available_copies', 0) > data.get('total_copies', 0):
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies"
            )
        return data


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    
    Handles the serialization and deserialization of Transaction objects,
    including the relationship between users and books.
    """
    days_overdue = serializers.IntegerField(read_only=True)
    penalty_amount = serializers.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        read_only=True
    )
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'book_title', 'checkout_date', 'due_date', 
            'return_date', 'days_overdue', 'penalty_amount', 
            'penalty_paid'
        ]
        read_only_fields = ['penalty_amount','penalty_paid', 'days_overdue']
        
    def validate(self, data):
        """
        Validate the transaction data.
        
        Ensures that:
        1. A book isn't checked out if it's unavailable
        2. A user doesn't exceed their checkout limit
        
        Args:
            data (dict): The data to validate
            
        Returns:
            dict: The validated data
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        book = data.get('book')
        user = data.get('user')
        
        if book and not book.is_available: 
            raise serializers.ValidationError("This book is not available")
            
        if user and Transaction.objects.filter(
            user=user, 
            return_date__isnull=True
        ).count() >= 1:
            raise serializers.ValidationError(
                "User has reached maximum checkout limit"
            )
            
        return data

class PenaltyPaymentSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(
        choices=['credit_card', 'debit_card', 'M-pesa'],
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Handles the serialization and deserialization of User objects,
    excluding sensitive information like passwords.
    """
    
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
        
    def create(self, validated_data):
        """
        Create and return a new user.
        
        Args:
            validated_data (dict): The validated data
            
        Returns:
            User: The created user instance
        """
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    
    Handles the serialization and deserialization of Profile objects,
    including the relationship with User objects.
    """
    
    # Nested serialization of user data
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ["id", "user", "profile_pic", "bio"]
        
    def validate_profile_pic(self, value):
        """
        Validate the profile picture.
        
        Args:
            value: The uploaded file
            
        Returns:
            File: The validated file
            
        Raises:
            serializers.ValidationError: If file is too large or wrong format
        """
        # Example validation - adjust based on your requirements
        if value.size > 1024 * 1024:  # 1MB
            raise serializers.ValidationError("Profile picture too large")
        return value