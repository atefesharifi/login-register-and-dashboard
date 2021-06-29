from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from apps.accounts.models.team import Team
from apps.accounts.models.team_user import TeamUser

User = get_user_model()


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password_1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password_2 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    file_resume = forms.FileField()

    def __str__(self):
        return self.user_name

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('user.exist')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email exists')
        return email

    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('password not match')
        elif len(password2) < 5:
            raise forms.ValidationError('password to short')
        elif not any(x.isupper() for x in password2):
            raise forms.ValidationError('پسورد باید حداقل یک حروف بزرگ داشته باشد')
        return password1


class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class MemberTeamForm(ModelForm):
    class Meta:
        model = TeamUser
        fields = ['first_name', 'last_name', 'file_resume']

class PhoneForm(models.Model):
    phone = forms.IntegerField()

class CodeForm(models.Model):
    code = forms.CharField()
