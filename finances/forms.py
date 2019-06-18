from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Transaction, Account, Transfer


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'account',
            'name',
            'date',
            'type',
            'category',
            'cost',
            'amount',
            'description'
        ]

    # def __init__(self, user, *args, **kwargs):
    #     super(TransactionForm, self).__init__(*args, **kwargs)
        # self.fields['account'].queryset = Account.objects.filter(author=user)


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency']


class TransferForm(ModelForm):
    class Meta:
        model = Transfer
        fields = [
            'source',
            'destination',
            'amount',
            'description',
        ]

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')

        if source == destination:
            msg = 'Source and destination values can not be the same!'
            self.add_error('destination', msg)
