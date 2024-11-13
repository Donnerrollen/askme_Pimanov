from django import forms
from django.views.decorators.csrf import csrf_exempt

class LoginForm(forms.Form):
    login = forms.CharField(max_length = 40)
    password = forms.CharField(max_length = 40)

class RegisterForm(forms.Form):
    login = forms.CharField(max_length = 40)
    password = forms.CharField(max_length = 40)
    repeat_password = forms.CharField(max_length = 40)
    email = forms.CharField(max_length = 40)
    login = forms.CharField(max_length = 40)
    nickname = forms.CharField(max_length = 40)

class AnswerForm(forms.Form):
    answer = forms.CharField(max_length = 5000)

class TitleForm(forms.Form):
    title = forms.CharField(max_length = 100)

class AskForm(forms.Form):
    title = forms.CharField(max_length = 100)
    text = forms.CharField(max_length = 5000)
    tags = forms.CharField(max_length = 255)