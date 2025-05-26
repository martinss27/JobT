from django.urls import path
from .views import (
    RegisterView, LoginView, 
login_page, show_token, register_page)

urlpatterns = [
   # api endpoints
    path('api/register/', RegisterView.as_view(), name='register'), #register new users
    path('api/login/', LoginView.as_view(), name='login'), #check if user exist and return token
   # html pages
    path('login/', login_page, name='login_page'), #login page for users
    path('register/', register_page, name='register_page'), #register page for users
    path('token/<str:token>/', show_token, name='show_token'), #show token to user after login
]