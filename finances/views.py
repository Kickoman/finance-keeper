from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Transaction, Account
from .forms import TransactionForm, AccountForm


# Create your views here.
def index(request):
    return HttpResponse('Hi there! Finance application is here.')


def list_transactions(request):
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied()

    transactions = Transaction.objects.order_by('-date')
    template = loader.get_template('finances/list.html')
    context = {
        'transactions' : transactions,
    }
    return HttpResponse(template.render(context, request))


def add_transaction(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # form = TransactionForm(request.POST, request.user)
        form = TransactionForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.author = request.user
            object.save()
            form.save_m2m()
            return HttpResponseRedirect('/finances/list?highlight=' + str(object.pk))
    else:
        # form = TransactionForm(request.user)
        form = TransactionForm()
    form.fields['account'].queryset = Account.objects.filter(author=request.user)
    return render(request, 'finances/add_transaction.html', {'form': form})


def add_account(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.author = request.user
            object.save()
            form.save_m2m()
            return HttpResponseRedirect('/accounts/details/')
    else:
        form = AccountForm()
    return render(request, 'finances/add_account.html', {'form': form})