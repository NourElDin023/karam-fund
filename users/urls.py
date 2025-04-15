from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout, name='logout'),
]