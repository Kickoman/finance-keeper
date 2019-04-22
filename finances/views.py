from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Transaction, Account, Category
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
        form = TransactionForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.author = request.user
            object.save()
            form.save_m2m()
            return HttpResponseRedirect('/finances/list?highlight=' + str(object.pk))
    else:
        form = TransactionForm()

    # Populating set of values only with allowed items (accounts of current user)
    form.fields['account'].queryset = Account.objects.filter(author=request.user)

    # Setting default value as latest used
    all_transactions = Transaction.objects.filter(
        author=request.user
    ).order_by('-date')

    if all_transactions:
        latest_used_account = all_transactions[0].account.pk
        form.initial = {'account': latest_used_account}

    # Lists of categories divided by their type
    # It's necessary for disabling items
    income_categories = Category.objects.filter(type=1)
    expense_categories = Category.objects.filter(type=0)

    return render(
        request,
        'finances/add_transaction.html',
        {
            'form': form,
            'incomes': income_categories,
            'expenses': expense_categories,
        }
    )


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