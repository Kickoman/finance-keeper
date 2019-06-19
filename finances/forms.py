from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Transaction, Account, Transfer


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionForm(forms.ModelForm):
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
        widgets = {
            'date': DateInput()
        }

    # def __init__(self, user, *args, **kwargs):
    #     super(TransactionForm, self).__init__(*args, **kwargs)
        # self.fields['account'].queryset = Account.objects.filter(author=user)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency']


class TransferForm(forms.ModelForm):
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
