from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name="Статус",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name="Автор",
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
        blank=True,
        null=True,
        verbose_name="Исполнитель",
    )
    labels = models.ManyToManyField(
        Label, related_name="tasks", blank=True, verbose_name="Метки"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]
