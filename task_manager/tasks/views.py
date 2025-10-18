from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"
    login_url = reverse_lazy("login")
    filterset_class = TaskFilter

    def get_queryset(self):
        return (
            Task.objects.all()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
            .order_by("-created_at")
        )

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {}
        return kwargs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    login_url = reverse_lazy("login")


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Задача успешно создана"
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create Task")
        return context


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Задача успешно изменена"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Task")
        return context


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Задача успешно удалена"
    login_url = reverse_lazy("login")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks_list")
