from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import CustomUserLoginForm, UserRegisterForm, UserUpdateForm
from .models import User


class UserListView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users_list")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users_list")

    def post(self, request, *args, **kwargs):
        try:
            result = super().post(request, *args, **kwargs)
            messages.success(self.request, "Пользователь успешно удален")
            return result
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return redirect(self.success_url)


class CustomLoginView(LoginView):
    form_class = CustomUserLoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    messages.info(request, "Вы разлогинены")
    return redirect("index")
