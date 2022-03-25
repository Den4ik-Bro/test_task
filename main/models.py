from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, PROTECT

User = get_user_model()


class Vacancy(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name='пользователь')
    vacancy_name = models.CharField(max_length=50, verbose_name='название вакансии')
    city = models.CharField(max_length=50, verbose_name='город')
    min_salary = models.PositiveSmallIntegerField(verbose_name='от', null=True, blank=True)
    max_salary = models.PositiveSmallIntegerField(verbose_name='до', null=True, blank=True)
    currency = models.CharField(max_length=10, verbose_name='валюта', null=True, blank=True)
    date_published = models.DateTimeField(verbose_name='дата публикации')
    url = models.URLField(verbose_name='ссылка на вакансию', null=True, blank=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return self.vacancy_name

