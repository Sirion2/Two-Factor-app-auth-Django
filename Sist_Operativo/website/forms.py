from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# from .models import Token

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=16, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class TokenForm(forms.Form):
    token = forms.CharField(max_length=6)