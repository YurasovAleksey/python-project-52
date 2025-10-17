import django_filters
from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        empty_label='---------'
    )
    
    executor = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('executor').remote_field.model.objects.all(),
        label='Исполнитель',
        empty_label='---------'
    )
    
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        empty_label='---------'
    )
    
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['executor'].queryset = self.filters['executor'].queryset.order_by('username')
        self.filters['labels'].queryset = self.filters['labels'].queryset.order_by('name')
