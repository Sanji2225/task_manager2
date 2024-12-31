from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from . import forms
from .forms import RegistroUser


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method !="POST":
        form = RegistroUser()
    else:
        form = RegistroUser(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse('index'))

    context = {'form': form}
    return render(request, 'users/register.html',context)
