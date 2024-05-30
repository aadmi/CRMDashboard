from django.db import models
from django.contrib.auth.models import User
import pyotp
import time


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = pyotp.TOTP(pyotp.random_base32()).now()
        self.timestamp = time.time()
        self.save()

    def verify_otp(self, otp):
        totp = pyotp.TOTP(pyotp.random_base32())
        return totp.verify(otp, for_time=self.timestamp)
