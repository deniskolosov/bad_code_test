from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


# Необходимо проверять есть ли достаточная сумма у пользователя,
# со счета которого списываются средства, и есть ли пользователи с указанным ИНН в БД.
# При валидности введенных данных необходимо указанную сумму списать со счета указанного пользователя
# и перевести на счета пользователей с указанным ИНН в равных частях
# (если переводится 60 рублей 10ти пользователям, то каждому попадет 6 рублей на счет).
# Обязательно наличие unit-тестов.

# get the user, get all of their accounts, where amount is > then given sum
# find all users having given tax ids,
# add necessary sum to user accounts

# add methods to account - top up, and  withdraw
from exceptions import NotEnoughMoney


class Account(models.Model):
    amount = models.DecimalField(decimal_places=2)
    user = models.ForeignKey(User, related_name="accounts", on_delete=models.CASCADE)

    def __str__(self):
        return 'Account for user {user}'.format(user=self.user)

    def top_up(self, top_up_amount: Decimal) -> None:
        """
        Tops up user account with top_up_amount of money.
        """
        self.amount += top_up_amount
        self.save()

    def withdraw(self, withdraw_amount: Decimal) -> None:
        """
        Withdraws withdraw_amount of money from user's account. If there is not, raises Exception.
        """
        if self.has_enough_money(withdraw_amount):
            self.amount -= withdraw_amount
            self.save()
        else:
            raise NotEnoughMoney()

    def has_enough_money(self, withdraw_amount: Decimal) -> bool:
        """
        Checks whether it's enough money on user's account.
        """
        return self.amount - withdraw_amount >= 0


class AccountUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='Пользователи')
    inn = models.IntegerField(verbose_name='ИНН')

    def __str__(self):
        return 'id={id}, inn={inn}'.format(id=str(self.id),
                                           inn=self.inn)
