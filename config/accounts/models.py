from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# custom manager class that handle user creation
class UserManager(BaseUserManager):
    # Method to create a new user(regular user)
    def create_user(self, email, first_name, last_name, username, password=None):
        # Ensure email is provided
        if not email:
            raise ValueError('Enter email address')
        # Ensure username is provided
        if not username:
            raise ValueError('Enter username')
        # Create a new user instance
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        # Set user password (hashed)
        user.set_password(password)
        # save the user instance into the database
        user.save(using=self._db)
        return user

    # Method to create a new superuser (admin user)
    def create_superuser(self, first_name,last_name, email, username, password):
        # use create_user method to create a new user
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            password=password, 
        )

        # set additional permissions for superuser
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# A custom user model that extends AbstractUser to add custom fields and behavior
class User(AbstractUser):
    # Additional fields
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255) 
    username = models.CharField(max_length=255, unique=True)
    date_of_membership = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    # Link to Custom manager
    objects = UserManager()
    
    # Set email as the field used for authentication
    USERNAME_FIELD = 'email'
    # Other required fields
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

# Profile model linked to the custom user model
class profile(models.Model):
    # Foreign key linking profile to user
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'