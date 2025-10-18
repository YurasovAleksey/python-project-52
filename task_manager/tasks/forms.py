from django import forms

from task_manager.labels.models import Label

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название задачи",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Описание задачи",
                    "rows": 4,
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "executor": forms.Select(attrs={"class": "form-control"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].required = False
        self.fields["executor"].queryset = self.fields[
            "executor"
        ].queryset.order_by("username")
        self.fields["labels"].queryset = Label.objects.all().order_by("name")
