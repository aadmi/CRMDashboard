from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import generate_otp_view, verify_otp_view

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_otp/', generate_otp_view, name='generate_otp'),
    path('verify_otp/', verify_otp_view, name='verify_otp'),
]