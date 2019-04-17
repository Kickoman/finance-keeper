from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Transaction, Account


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

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(author=user)