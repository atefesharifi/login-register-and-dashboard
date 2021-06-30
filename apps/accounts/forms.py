from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from apps.accounts.models.team import Team
from apps.accounts.models.team_user import TeamUser
from common.validators import FARSI_LANGUAGE

User = get_user_model()


class UserLoginForm(forms.Form):
    en_name = forms.CharField(max_length=23)


class UserOTPForm(forms.Form):
    code = forms.CharField(max_length=4)


class TeamRegisterForm(ModelForm):
    class Meta:
        model = Team
        fields = ['en_name', 'fa_name', 'phone']


class MemberTeamForm(ModelForm):
    class Meta:
        model = TeamUser
        fields = ['first_name', 'last_name', 'file_resume']


class AdminTeamForm(forms.Form):
    first_name = forms.CharField(max_length=20, validators=[FARSI_LANGUAGE])
    last_name = forms.CharField(max_length=25, validators=[FARSI_LANGUAGE])
    file_resume = forms.FileField()
    email = forms.CharField(max_length=40)
