from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginForm(forms.Form):
    en_name = forms.CharField(max_length=23)
    remember_me = forms.BooleanField(required=False)


class UserOTPForm(forms.Form):
    code = forms.CharField(max_length=4)
