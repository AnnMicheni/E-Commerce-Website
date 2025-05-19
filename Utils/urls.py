from django.urls import path
from .views import create_user, login, logout, verify_reset_otp, send_otp, send_reset_otp, verify_register_otp, send_register_otp

urlpatterns = [
    path('create-user/', create_user, name='create-user'),
    path('register/', send_register_otp, name='register'),
    path('register-otp/', verify_register_otp, name='register-otp'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('send-otp/', send_otp, name='send-otp'),
    path('verify/', verify_reset_otp, name='verify_otp'),
    path('send_reset_otp/', send_reset_otp, name='send_reset_otp'),
]
