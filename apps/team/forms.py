from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

from apps.team.models.team import Team
from apps.team.models.team_user import TeamUser
from common.validators import FARSI_LANGUAGE


class TeamRegisterForm(ModelForm):
    class Meta:
        model = Team
        fields = ['en_name', 'fa_name', 'phone']


class MemberTeamForm(ModelForm):
    class Meta:
        model = TeamUser
        fields = ['first_name', 'last_name', 'file_resume']


class AdminTeamForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'file_resume')
    # first_name = forms.CharField(max_length=20, validators=[FARSI_LANGUAGE])
    # last_name = forms.CharField(max_length=25, validators=[FARSI_LANGUAGE])
    # file_resume = forms.FileField(required=False)


class CodeForm(ModelForm):
    class Meta:
        model = Team
        fields = ['id', 'code']
