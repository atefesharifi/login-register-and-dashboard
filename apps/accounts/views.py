from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View

from common.utilities import set_otp_cache
from .forms import *
from apps.team.forms import TeamRegisterForm
from apps.team.models import Team

User = get_user_model()


def register(request):
    """Create and return a `Team` with an english name(en_name), persian name(fa_name) and phone."""
    if request.method == 'POST':
        team_form = TeamRegisterForm(request.POST)
        if team_form.is_valid():
            data = team_form.cleaned_data
            team = Team.objects.create(fa_name=data['fa_name'], en_name=data['en_name'], phone=data['phone'])
            phone = team.phone
            code = randint(1000, 9999)
            print(code)
            set_otp_cache(team.id, code)
            messages.success(request, 'رمز عبور یکبار مصرف ارسال شد', 'success')
            # send_smd(code, phone)
            return redirect('accounts:second_login', team.id)
        else:
            messages.error(request, 'لطفا اطلاعات صحیح وارد کنید', 'secondary')
            return render(request, 'accounts/register.html', {'team_form': team_form})

    else:
        team_form = TeamRegisterForm()

    context = {'team_form': team_form}
    return render(request, 'accounts/register.html', context)


class OTPLogin(View):
    """class for insert OTP and then if pass is correct,login team admin"""

    def get(self, request, pk):
        team = get_object_or_404(Team, id=pk)
        form = UserOTPForm()
        return render(request, 'accounts/second_login.html', {'form': form, 'pk': pk, 'phone_number': team.phone})

    def post(self, request, pk):
        url = request.META.get('HTTP_REFERER')
        form = UserOTPForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(id=pk)
            validated_data = form.cleaned_data
            cache_team = cache.get(key=team.id)
            if cache_team is not None:
                if validated_data['code'] == cache_team['code']:
                    if len(User.objects.filter(team=team)) != 0:
                        user = User.objects.get(team=team)
                        authenticate(request, username=user.username, password=user.password)
                        login(request, user)
                        team.verify_phone = True
                        team.save()
                        return redirect('team:home')
                    else:
                        user = User(username=team.en_name, team=team)
                        user.set_password('1234')
                        user.save()
                        authenticate(request, username=user.username, password=user.password)
                        login(request, user)
                        # ??????????????????????????????????????????????????????????????????????????????????????????
                        return redirect('team:home')

                else:
                    messages.error(request, 'کد وارد شده صحیح نیست', 'danger')
                    return redirect(url)
            else:
                messages.error(request, 'کد منقضی شده است', 'warning')
                return redirect(url)
        else:
            messages.error(request, 'اطلاغات وارد شده نادرست می باشد.', 'secondary')
            return redirect(url)


def pass_duplicate(request, pk):
    """ this function send OTP again in second_login html page"""
    team = Team.objects.get(id=pk)
    phone = team.phone
    code = randint(1000, 9999)
    print(code)
    set_otp_cache(team.id, code)
    messages.success(request, 'رمز عبور یکبار مصرف ارسال شد', 'success')
    # send_smd(code, phone)
    return redirect('accounts:second_login', pk=team.id)


class Login(View):
    """
    this class enable team admin to login with phone number
    and then send a otp that admin must insert this code in
    another page that name is OTPLogin
    """

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_name = data['en_name']
            if Team.objects.filter(en_name=user_name).count() == 0:
                messages.success(request, 'تیم با این نام موجود نیست لطفا ابتدا ثبت نام کنید', 'warning')
                return redirect('accounts:login')
            team = Team.objects.get(en_name=user_name)
            phone = team.phone
            code = randint(1000, 9999)
            print(code)
            set_otp_cache(team.id, code)
            # send_smd(code, phone)
            return redirect('accounts:second_login', pk=team.id)
        else:
            messages.success(request, 'اطلاعات وارد شده نادرست است', 'secondary')
            return render(request, 'accounts/login.html', {'form': form})

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='login')
def user_logout(request):
    django_logout(request)
    messages.success(request, 'با موفقیت خارج شدید', 'success')
    return redirect('accounts:login')
