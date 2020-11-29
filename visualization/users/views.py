from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserRegisterFrom

def register(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created') 
            return HttpResponseRedirect('/login/')
    else:   
        form = UserRegisterFrom()

    return render(request,'users/register.html',{'form':form})