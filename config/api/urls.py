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

# Create a router and register viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CheckoutBookView.as_view(), name='checkout-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),

]
