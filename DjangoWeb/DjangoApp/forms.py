from django import forms
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from .models import Post


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email','class': 'forget-pass-box-email','placeholder':'Email address'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Please Input Password'}),
    )
    new_password2 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Please Input Password Again'}),
    )
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'star', 'address', 'image']

    
    
    