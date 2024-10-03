from django.urls import path
from . import views


urlpatterns = [
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.CustomLoginView.as_view(), name='login'),  # new path
]
 