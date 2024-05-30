from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
from CRMFinance.CRMFinance import settings


@api_view(['POST'])
def generate_otp_view(request):
    email = request.data.get('email')
    user = User.objects.get(email=email)
    otp_instance, created = OTP.objects.get_or_create(user=user)
    otp_instance.generate_otp()
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp_instance.otp}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return Response({'message': 'OTP sent'})


@api_view(['POST'])
def verify_otp_view(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp')
    try:
        user = User.objects.get(email=email)
    except AttributeError:
        return Response({'message': 'User not found'}, status=404)

    try:
        otp_instance = OTP.objects.get(user=user)
    except AttributeError:
        return Response({'message': 'OTP not found'}, status=404)

    if otp_instance.verify_otp(otp_code):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.token
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
        })
    else:
        return Response({'message': 'Invalid OTP'}, status=400)
