from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.core import serializers
from json import dumps


from .forms import SigninForm, SignupForm


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