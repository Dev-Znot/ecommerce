from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username", "class":"form-control border-0 border-bottom rounded-0", "id":"username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"name@example.com", "class":"form-control border-0 border-bottom rounded-0", "id":"email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password", "class":"form-control border-0 border-bottom rounded-0", "id":"password1"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password again", "class":"form-control border-0 border-bottom rounded-0", "id":"password2"}))


    class Meta:
        model = User
        fields = ["username", "email"]