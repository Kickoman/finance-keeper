from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'date', 'type', 'category', 'cost', 'amount', 'description']