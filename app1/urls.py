from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path('home', home, name ='home'),
    path('home/<int:entity_id>', user_details, name='user_details'),
    path('login', log_in, name ='login'),
    path('logout', log_out, name='logout'),
    path('register', register, name='register'),
]
# webapp/urls.py




