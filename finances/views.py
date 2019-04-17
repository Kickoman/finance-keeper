from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Transaction
from .forms import TransactionForm

# Create your views here.

# TODO: read this:
# Well, user authentication system has been added
# Now it's time to add transaction system

def index(request):
    return HttpResponse('Hi there! Finance application is here.')


def list(request):
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
    # template = loader.get_template('finances/add_transaction.html')

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # object = Transaction(form.cleaned_data)
            # object.save()
            object = form.save(commit=False)
            object.author = request.user
            object.save()
            form.save_m2m()
            return HttpResponseRedirect('/finances/list?highlight=' + str(object.pk))
    else:
        form = TransactionForm()
    return render(request, 'finances/add_transaction.html', {'form': form})


def submission(request):
    return HttpResponse("Submission page")