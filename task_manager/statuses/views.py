from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


class StatusListView(ListView):
    model = Status
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses"


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_list")
    success_message = "Статус успешно изменен"


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_list")
    success_message = "Статус успешно удален"
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request, "Невозможно удалить статус, потому что он используется"
            )
            return redirect("statuses_list")
