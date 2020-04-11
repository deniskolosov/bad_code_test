from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    amount = models.DecimalField(decimal_places=2)
    user = models.ForeignKey(User, related_name="accounts", on_delete=models.CASCADE)

    def __str__(self):
        return 'Account for user {user}'.format(user=self.user)


class AccountUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='Пользователи')
    inn = models.IntegerField(verbose_name='ИНН')

    def __str__(self):
        return 'id={id}, inn={inn}'.format(id=str(self.id),
                                           inn=self.inn)
