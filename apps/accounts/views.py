from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import get_user_model
from random import randint
from kavenegar import *

User = get_user_model()


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['user']), password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود با موفقیت انجام شد', 'primary')
                return redirect('home')
            else:
                messages.error(request, 'user or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        adminform = UserRegisterForm(request.POST, request.FILES)
        teamform = TeamForm(request.POST)
        if adminform.is_valid() and teamform.is_valid():
            data1 = adminform.cleaned_data
            data2 = teamform.cleaned_data
            team = Team.objects.create(fa_name=data2['fa_name'], en_name=data2['en_name'], phone=data2['phone'])
            User.objects.create_user(username=data1['user_name'], email=data1['email'], first_name=data1['first_name'],
                                     last_name=data1['last_name'], password=data1['password_2'],
                                     file_resume=data1['file_resume'], team=team)
            messages.success(request, 'ثبت نام با موفقیت انجام شد', 'primary')
            return redirect('home')
    else:
        adminform = UserRegisterForm()
        teamform = TeamForm()

    context = {'adminform': adminform, 'teamform': teamform}
    return render(request, 'accounts/register.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید', 'success')
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
        team_form = TeamForm(request.POST, instance=request.user.team)
        member_form = MemberTeamForm(request.POST)
        if team_form.is_valid():
            team_form.save()
            messages.success(request, 'update successfully', 'success')
            return redirect('teamprofile')
        else:
            messages.error(request, "Error")
    else:
        team_form = TeamForm(instance=request.user.team)
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

def login_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            global random_code
            data=form.cleaned_data
            phone = data['phone']
            # random_code = randint(100,1000)           
            api = KavenegarAPI('4442494F6A77766776746B3444575466373961693741335956544F6B45683669556B6C7731493538534A413D')
            params = { 'sender' : '1000596446', 'receptor': '09918434990', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
            response = api.sms_send( params)
            return redirect('accounts:verify')
    else:
        form = PhoneForm()
    return render(request,'accounts/loginphone.html',{'form':form})

def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            if random_code == 
    else:
        pass
    return render(requuet,'accounts/code.html',{'form':form})
