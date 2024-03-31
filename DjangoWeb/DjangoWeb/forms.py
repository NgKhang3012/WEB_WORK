from django import forms

class RegistrationForm(forms.Form):
    email_or_phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email address or phone number', 'class':'box_input_text_account_Reg',}),label='')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Please Input Password', 'class':'box_input_text_password_Reg'}),label='')
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Please Input Password Again','class':'box_input_text_password_Reg'}),label='')
    
class LoginForm(forms.Form):
    email_or_phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email address or phone number', 'class':'box_input_text_account_Reg',}),label='')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Please Input Password', 'class':'box_input_text_password_Reg'}),label='')
