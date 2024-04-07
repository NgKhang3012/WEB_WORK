from django import forms
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email','class': 'forget-pass-box-email','placeholder':'Nhập email của bạn'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Nhập mật khẩu của bạn'}),
    )
    new_password2 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Nhập lại mật khẩu của bạn'}),
    )
    
