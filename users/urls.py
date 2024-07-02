# users/urls.py
from django.urls import path
from .views import (
    RegisterEmployeeView,
    RegisterCustomerView,
    CurrentUserView,
    UserDetailView,

)

urlpatterns = [
    # registration
    path('register-employee/', RegisterEmployeeView.as_view(), name='register-employee'),
    path('register-customer/', RegisterCustomerView.as_view(), name='register-employee'),

    # user info
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('<uuid:pk>/', UserDetailView.as_view(), name='employee-detail'),
]
