from random import randint
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView

from common.utilities import send_smd, set_otp_cache
from .forms import *
from django.contrib.auth import authenticate, login

User = get_user_model()


def register(request):
    """Create and return a `Team` with an english name(en_name), persian name(fa_name) and phone."""
    if request.method == 'POST':
        team_form = TeamRegisterForm(request.POST)
        if team_form.is_valid():
            data = team_form.cleaned_data
            team = Team.objects.create(fa_name=data['fa_name'], en_name=data['en_name'], phone=data['phone'])
            messages.success(request, 'تیم با موفقیت ثبت شد', 'primary')
            phone = team.phone
            code = randint(1000, 9999)
            print(code)
            set_otp_cache(team.id, code)
            # send_smd(code, phone)
            return redirect('accounts:second_login', team.id)
        else:
            messages.error(request, 'لطفا اطلاعات صحیح وارد کنید', 'secondary')
            return render(request, 'accounts/register.html', {'team_form': team_form})

    else:
        team_form = TeamRegisterForm()

    context = {'team_form': team_form}
    return render(request, 'accounts/register.html', context)


class Login(View):
    """ this class enable team admin to login with phone number and then send a otp that admin must insert this code in another page that name is OTPLogin"""
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_name = data['en_name']
            if Team.objects.filter(en_name=user_name).count() == 0:
                messages.success(request, 'ابتدا ثبت نام کنید', 'warning')
                return redirect('accounts:register')
            team = Team.objects.get(en_name=user_name)
            phone = team.phone
            code = randint(1000, 9999)
            print(code)
            set_otp_cache(team.id, code)
            # send_smd(code, phone)
            return redirect('accounts:second_login', pk=team.id)
        else:
            messages.success(request, 'لطفا نام تیم خود را وارد کنید', 'secondary')
            return render(request, 'accounts/login.html', {'form': form})

    def get(self, request):     
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})


class OTPLogin(View):
    """this class is for insert OTP"""
    def get(self, request, pk):
        messages.success(request, 'رمز عبور یکبار مصرف ارسال شد', 'success')
        form = UserOTPForm()
        return render(request, 'accounts/second_login.html', {'form': form,'pk':pk})

    def post(self, request, pk):       
        form = UserOTPForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(id=pk)
            validated_data = form.cleaned_data
            cache_team = cache.get(key=team.id)
            if not cache_team == None:
                if validated_data['code'] == cache_team['code']:
                    if len(User.objects.filter(team=team)) != 0:
                        user = User.objects.get(team=team)
                        authenticate(request, username=user.username, password=user.password)
                        login(request, user)
                        team.verify_phone = True
                        team.save()
                        return redirect('home:home')
                    else:
                        user = User(username=team.en_name, team=team)
                        user.set_password('1234')
                        user.save()
                        authenticate(request, username=user.username, password=user.password)
                        login(request, user)
                        return redirect('home:home')

                else:
                    messages.success(request, 'کد وارد شده صحیح نیست', 'danger')
                    return render(request, 'accounts/second_login.html', {'form': form})
            else:
                messages.success(request, 'کد منقضی شده است', 'warning')
                return render(request, 'accounts/second_login.html', {'form': form})
        else:
            messages.error(request, 'لطفا رمز عبور را وارد کنید', 'secondary')
            return render(request, 'accounts/second_login.html',{'form': form})


@login_required(login_url='login')
def user_logout(request):
    django_logout(request)
    messages.success(request, 'با موفقیت خارج شدید', 'success')
    return redirect('home:home')


@login_required(login_url='login')
def team_profile(request):
    team = request.user.team
    member = TeamUser.objects.filter(team=team)
    return render(request, 'accounts/teamprofile.html', {'team': team, 'member': member})


@login_required(login_url='accounts:login')
def add_member(request):
    """this function is for add team member that needs first name,last name and CV"""
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
                    messages.success(request, 'عضو تیم با موفقیت اضافه شد', 'success')
                else:
                    messages.error(request, 'عضو تیم قبلا اضافه شده است', 'warning')
            else:
                messages.error(request, 'اسامی معتبر نیستند', 'danger')

        else:
            messages.error(request, 'مجاز به اضافه کردن بیش از 5 نفر نیستید', 'danger')
    else:
        form = MemberTeamForm()
    return redirect(url)


@login_required(login_url='login')
def team_update(request):
    """this function update team profile that consist of member team,admin team and team specifications"""
    team = request.user.team
    member = TeamUser.objects.filter(team=team)
    if request.method == 'POST':
        team_form = TeamRegisterForm(request.POST, instance=request.user.team)
        member_form = MemberTeamForm(request.POST)
        admin_form = AdminTeamForm(request.POST)
        if team_form.is_valid():
            team_form.save()
            user = User.objects.get(id=request.user.id)
            user.username = team.en_name
            user.save()
            messages.success(request, 'به روز رسانی انجام شد', 'success')
            return redirect('accounts:teamprofile')
        else:
            messages.error(request, 'به دلیل اطلاعات نادرست به روز رسانی انجام نشد', 'warning')
            return redirect('accounts:update')

    else:
        team_form = TeamRegisterForm(instance=request.user.team)
        member_form = MemberTeamForm()
        user = User.objects.get(id=request.user.id)
        data_user = {'first_name': user.first_name, 'last_name': user.last_name,
                     'email': user.email}
        admin_form = AdminTeamForm(
            initial=data_user)
    context = {'team': team, 'member': member, 'team_form': team_form, 'member_form': member_form,
               'admin_form': admin_form}
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
def update_admin(request):
    """this function update team admin specifications that consist first name,last name and CV"""
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AdminTeamForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            if data['file_resume']:
                user.file_resume = data['file_resume']
            user.email = data['email']
            user.save()
            messages.success(request, 'به روز رسانی اطلاعات مدیر تیم با موفقیت انجام شد', 'primary')
        else:
            messages.error(request, 'اسامی فارسی وارد شود','warning')

    return redirect(url)

def pass_duplicate(request,pk):
    """ this function send OTP again in second_login html page"""
    team = Team.objects.get(id=pk)
    phone = team.phone
    code = randint(1000, 9999)
    print(code)
    set_otp_cache(team.id, code)
    # send_smd(code, phone)
    return redirect('accounts:second_login', pk=team.id)


