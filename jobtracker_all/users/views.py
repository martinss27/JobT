from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model, authenticate, login, logout
from django import forms

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data) 
        if serializer.is_valid(): 
            user = serializer.validated_data 
            token, created = Token.objects.get_or_create(user=user)
            print('token:', token)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"detail": "Logout completed successfully."}, status=status.HTTP_200_OK)



# (django registration and login views using forms)
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_page')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def login_page(request):
    token = None
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return redirect('show_token',token=token.key)
        else:
            form.add_error(None, "Invalid username or password.")
    return render(request, 'users/login.html', {'form': form})

def show_token(request, token):
    return render(request, 'users/show_token.html', {'token': token})