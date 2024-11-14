from django import forms
from auth_app.models import *

class LoginForm(forms.Form):
    userid = forms.CharField(max_length=20, label='UserID',
                            widget = forms.TextInput(attrs={'placeholder': 'Enter your ID', 'autocomplete': 'off'}),
                            required=True)

    password = forms.CharField(max_length=20, label='Password', 
                               widget=forms.PasswordInput(attrs={'placeholder' : 'Enter your Password', 'autocomplete': 'off'}), 
                               required=True)