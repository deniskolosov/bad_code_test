from django.contrib.auth.models import User
from django.db import models


class AccountUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='Пользователи')
    inn = models.IntegerField(verbose_name='ИНН')
    account = models.FloatField(verbose_name='Счeта')

    def __str__(self):
        return 'id={id}, inn={inn}'.format(id=str(self.id),
                                           inn=self.inn)
