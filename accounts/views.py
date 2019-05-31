from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.core import serializers
from json import dumps
from django.template import loader

from .forms import SigninForm, SignupForm
from finances.models import Account, Transaction

from decimal import Decimal


# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.INFO, 'Wrong login or passwd')

    else:
        form = SigninForm()
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            try:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                user.save()
                return redirect('accounts:sign_in')
            except IntegrityError: # someone registered before with ur name
                messages.add_message(request, messages.ERROR, 'Database error, try once again')
        else:
            messages.add_message(request, messages.INFO, "Form is invalid")
    else:
        form = SignupForm()
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def details(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    balances = {}
    current_balance = Decimal(0)
    all_transactions = Transaction.objects.filter(
        author=request.user
    )

    for t in all_transactions:
        cur = t.account.currency
        factor = 1 if t.type else -1
        if cur in balances:
            balances[cur] += t.cost * t.amount * factor
        else:
            balances[cur] = t.cost * t.amount * factor

    accounts = Account.objects.filter(author=request.user)

    template = loader.get_template('accounts/details.html')
    context = {
        'accounts': accounts,
        'balance': balances
    }
    return HttpResponse(template.render(context, request))