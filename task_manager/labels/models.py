from django.db import models
from django.db.models import ProtectedError


class Label(models.Model):
    name = models.CharField(
        max_length=150, blank=False, unique=True, verbose_name="Имя"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise ProtectedError(
                "Нельзя удалить метку, так как она используется в задачах",
                self.tasks.all(),
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"
