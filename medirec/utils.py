from django.core.cache import cache
from datetime import timedelta
import random

#Ganerate a random OTP linked to a user and save it to cache
def create_OTP(username):
    otp = random.randint(100000,999999)
    cache.set(username,otp, timeout=300)
    return otp

#Get OTP user and compare to saved OTP
def verify_OTP(username, code):
    cached_code = cache.get(username)
    return str(cached_code) == str(code)