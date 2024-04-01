from django.shortcuts import render, redirect
from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView 
from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'Forget_password/Forget_password.html'
    success_url='done'
    form_class = CustomPasswordResetForm
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name= 'Password_Reset_Done/Password_Reset_Done.html'    

class CustomPasswordConfirmView(PasswordResetConfirmView):
    template_name= 'Password_Reset_Confirm/Password_Reset_Confirm.html' 
    form_class= CustomSetPasswordForm   
    
def index(request):
    if request.method == 'POST':
        if 'button-login' in request.POST:
            email_or_phone = request.POST.get('input-login-account')
            password = request.POST.get('input-login-password')
            user = authenticate(request, username=email_or_phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('whilelogin') 
            else:
                return render(request, 'index.html', {'error_message': 'Invalid email/phone number or password'})
        elif 'button-reg' in request.POST:
            email_or_phone = request.POST.get('input-reg-account')
            password = request.POST.get('input-reg-password')
            confirm_password = request.POST.get('input-reg-repassword')
            if password != confirm_password:
                return render(request, 'index.html', {'error_message': 'Passwords do not match'})
            user = User.objects.create_user(username=email_or_phone, password=password)
            user.save()
            return redirect('whilelogin')
    else:
        return render(request, 'index.html')

def whilelogin(request):
    return render(request,'While_Login/index-login.html')

def verifyotp(request):
    return render(request,'verify_otp/verify_otp.html')