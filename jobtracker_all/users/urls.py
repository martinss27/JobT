from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
login_page, show_token, register_page)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
    )

urlpatterns = [
   # api endpoints
    path('register/', RegisterView.as_view(), name='register'), #register new users
    path('login/', LoginView.as_view(), name='login'), #check if user exist and return token
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #get token for user
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #refresh token for user
   # html pages
    path('f/login/', login_page, name='login_page'), #login page for users
    path('f/register/', register_page, name='register_page'), #register page for users
    path('f/token/<str:token>/', show_token, name='show_token'), #show token to user after login
]