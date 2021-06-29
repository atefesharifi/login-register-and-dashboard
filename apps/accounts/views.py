from random import randint

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views import View

from common.utilities import send_smd, set_otp_cache
from .forms import *

User = get_user_model()


class Login(View):
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_name = data['en_name']
            if Team.objects.filter(en_name=user_name).count() == 0:
                messages.success(request, 'ابتدا ثبت نام کنید', 'warning')
                return redirect('register')
            team = Team.objects.get(en_name=user_name)
            phone = team.phone
            code = randint(1000, 9999)
            print(code)
            set_otp_cache(team.id, code)
            send_smd(code, phone)
            return redirect('second_login', pk=team.id)
        else:
            messages.success(request, 'لطفا نام تیم خود را وارد کنید', 'primary')
            return render(request, 'accounts/login.html', {'form': form})

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})


class OTPLogin(View):
    def get(self, request, pk):
        form = UserOTPForm()
        return render(request, 'accounts/second_login.html', {'form': form})

    def post(self, request, pk):
        form = UserOTPForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(id=pk)
            validated_data = form.cleaned_data
            cache_team = cache.get(key=team.id)
            if not cache_team == None:
                if validated_data['code'] == cache_team['code']:
                    request.session['team_id'] = team.id
                    return redirect('teamprofile')
                else:
                    messages.success(request, 'کد وارد شده صحیح نیست', 'primary')
                    return render(request, 'accounts/second_login.html', {'form': form})
            else:
                messages.success(request, 'کد منقضی شده', 'primary')
                return render(request, 'accounts/second_login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        team_form = TeamRegisterForm(request.POST)
        if team_form.is_valid():
            data = team_form.cleaned_data
            team = Team.objects.create(fa_name=data['fa_name'], en_name=data['en_name'], phone=data['phone'])
            messages.success(request, '؟؟', 'primary')
            phone = team.phone
            code = randint(1000, 9999)
            print(code)
            set_otp_cache(team.id, code)
            send_smd(code, phone)
            return redirect('second_login', team.id)
    else:
        team_form = TeamRegisterForm()

    context = {'team_form': team_form}
    return render(request, 'accounts/register.html', context)


class Logout(View):
    def get(self, request):
        try:
            del request.session['team_id']
        except KeyError:
            pass
        return redirect('home')


@login_required(login_url='accounts:login')
def team_profile(request):
    team = request.user.team
    member = TeamUser.objects.filter(team=team)

    return render(request, 'accounts/teamprofile.html', {'team': team, 'member': member})


@login_required(login_url='accounts:login')
def add_member(request):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    team = user.team
    member_count = team.mteam.all().count()
    if request.method == 'POST':
        if member_count < 5:
            form = MemberTeamForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                if not TeamUser.objects.filter(first_name=data['first_name'], last_name=data['last_name'], team=team):
                    TeamUser.objects.create(team=team, first_name=data['first_name'], last_name=data['last_name'],
                                            file_resume=data['file_resume'])
                    messages.success(request, 'عضو تیم با موفقیت اضافه شد', 'primary')
                else:
                    messages.error(request, 'عضو تیم قبلا اضافه شده است', 'danger')

        else:
            messages.error(request, 'مجاز به اضافه کردن بیش از 5 نفر نیستید', 'danger')
    else:
        form = MemberTeamForm()
    return redirect(url)


@login_required(login_url='login')
def team_update(request):
    team = request.user.team
    member = TeamUser.objects.filter(team=team)
    if request.method == 'POST':
        team_form = TeamRegisterForm(request.POST, instance=request.user.team)
        member_form = MemberTeamForm(request.POST)
        if team_form.is_valid():
            team_form.save()
            messages.success(request, 'update successfully', 'success')
            return redirect('teamprofile')
        else:
            messages.error(request, "Error")
    else:
        team_form = TeamRegisterForm(instance=request.user.team)
        member_form = MemberTeamForm()

    context = {'team': team, 'member': member, 'team_form': team_form, 'member_form': member_form}
    return render(request, 'accounts/update.html', context)


@login_required(login_url='login')
def remove_member(request, id):
    url = request.META.get('HTTP_REFERER')
    user = User.objects.get(id=request.user.id)
    team = user.team
    member = team.mteam.get(id=id)
    member.delete()
    messages.success(request, 'عضو تیم با موفقیت حذف شد', 'primary')
    return redirect(url)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'پسورد با موفقیت تغییر کرد', 'success')
            return redirect('home')
        else:
            messages.error(request, 'پسورد درست انتخاب نشده است', 'danger')
            return redirect('change')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change.html', {'form': form})
