from django import forms

from .models import AccountUser


class TransferForm(forms.Form):
    user_from = forms.ModelChoiceField(queryset=AccountUser.objects.all(), empty_label='От кого')
    inn_to = forms.IntegerField(label='Кому')
    amount = forms.FloatField()
