from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        if 'button-login' in request.POST:
            email_or_phone = request.POST.get('input-login-account')
            password = request.POST.get('input-login-password')
            user = authenticate(request, username=email_or_phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the same page after login
            else:
                return render(request, 'index.html', {'error_message': 'Invalid email/phone number or password'})
        elif 'button-reg' in request.POST:
            email_or_phone = request.POST.get('input-reg-account')
            password = request.POST.get('input-reg-password')
            confirm_password = request.POST.get('input-reg-repassword')
            if password != confirm_password:
                return render(request, 'index.html', {'error_message': 'Passwords do not match'})
            user = User.objects.create_user(email_or_phone, email_or_phone, password)
            user.save()
            return redirect('index')
    else:
        return render(request, 'index.html')
