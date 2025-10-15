from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

class UsersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users.html')
