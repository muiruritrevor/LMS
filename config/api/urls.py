# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from api.views import (
#     BookViewSet,
#     UserViewSet,
#     ProfileViewSet,
#     TransactionViewSet,
#     CheckoutBookView,
#     ReturnBookView,
#     AvailableBooksView
# )

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'books', BookViewSet)
# router.register(r'users', UserViewSet)
# router.register(r'profiles', ProfileViewSet)
# router.register(r'transactions', TransactionViewSet)

# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('books/available/', AvailableBooksView.as_view(), name='available-books'),
#     path('checkout/', CheckoutBookView.as_view(), name='checkout-book'),
#     path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, 
    TransactionViewSet, 
    UserViewSet, 
    ProfileViewSet,
    CheckoutBookView,
    ReturnBookView
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    
    path('checkout/', CheckoutBookView.as_view(), name='checkout-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
]