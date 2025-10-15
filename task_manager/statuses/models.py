from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Имя'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
