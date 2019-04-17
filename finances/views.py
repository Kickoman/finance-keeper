from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Transaction
from .forms import TransactionForm


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
        form = TransactionForm(request.POST, request.user)
        if form.is_valid():
            object = form.save(commit=False)
            object.author = request.user
            object.save()
            form.save_m2m()
            return HttpResponseRedirect('/finances/list?highlight=' + str(object.pk))
    else:
        form = TransactionForm(request.user)
    return render(request, 'finances/add_transaction.html', {'form': form})


def submission(request):
    return HttpResponse("Submission page")