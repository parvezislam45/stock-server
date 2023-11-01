from django.urls import path
from .views import user_register, user_login, Profile

urlpatterns = [
    path('register/', user_register, name='user-register'),
    path('login/', user_login, name='user-login'),
    path('profile/', Profile.as_view(), name='profile')
]

