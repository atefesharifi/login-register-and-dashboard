from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import MemberTeamForm, TeamRegisterForm, AdminTeamForm, CodeForm
from .models import Rules, TeamUser, FrequentlyQuestions

User = get_user_model()


@login_required(login_url='login')
def home(request):
    team = request.user.team
    return render(request, 'team/home.html', {'team': team})


@login_required(login_url='login')
def team_profile(request):
    team = request.user.team
    member = TeamUser.objects.filter(team=team)
    return render(request, 'team/profile.html', {'team': team, 'member': member})


@login_required(login_url='login')
def frequently_question(request):
    team = request.user.team
    questions = FrequentlyQuestions.objects.all()
    return render(request, 'team/frequently_questions.html', {'team': team, 'questions': questions})


@login_required(login_url='login')
def result(request):
    team = request.user.team
    return render(request, 'team/result.html', {'team': team})


@login_required(login_url='login')
def get_content(request):
    team = request.user.team
    return render(request, 'team/get_content.html', {'team': team})


@login_required(login_url='login')
def sent_code(request):
    team = request.user.team
    return render(request, 'team/code.html', {'team': team, "file_name": team.code})


@login_required(login_url='login')
def team_update(request):
    """this function update team profile that consist of member team,admin team and team specifications"""
    team = request.user.team
    member = TeamUser.objects.filter(team=team)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        team_form = TeamRegisterForm(request.POST, instance=team)
        member_form = MemberTeamForm(request.POST)
        admin_form = AdminTeamForm(request.POST, request.FILES, instance=user)
        if team_form.is_valid() and admin_form.is_valid():
            team_form.save()
            admin_form.save()
            messages.success(request, 'به روز رسانی انجام شد', 'success')
            return redirect('team:team_profile')
        else:
            messages.error(request, 'به دلیل اطلاعات نادرست به روز رسانی انجام نشد', 'warning')
            return redirect('team:team_profile')

    else:
        team_form = TeamRegisterForm(instance=request.user.team)
        member_form = MemberTeamForm()
        admin_form = AdminTeamForm(instance=user)
        context = {'team': team, 'members': member, 'team_form': team_form, 'member_form': member_form,
                   'admin_form': admin_form, 'admin': request.user}
        return render(request, 'team/profile.html', context)


@csrf_exempt
@login_required(login_url='accounts:login')
def add_member(request):
    """this function is for add team member that needs first name,last name and CV"""
    team = request.user.team
    member_count = team.mteam.all().count()
    if request.method == 'POST':
        print("add member")
        if member_count < 5:
            form = MemberTeamForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                if not TeamUser.objects.filter(first_name=data['first_name'], last_name=data['last_name'], team=team):
                    team_user = TeamUser.objects.create(team=team, first_name=data['first_name'],
                                                        last_name=data['last_name'],
                                                        file_resume=data['file_resume'])
                    return JsonResponse(
                        {'id': team_user.id, 'fulname': team_user.first_name + ' ' + team_user.last_name,
                         'member_count': team.mteam.count()})
                else:
                    return HttpResponseBadRequest('عضو تیم قبلا اضافه شده است')
            else:
                return HttpResponseBadRequest('اطلاعات وارد شده صحیح نمی باشد')

        else:
            return HttpResponseBadRequest('مجاز به اضافه کردن بیش از 5 نفر نیستید')


@login_required(login_url='accounts:login')
def get_members(request):
    if request.method == 'GET':
        team = request.user.team
        # members = {'{}'.format(member.id): {'full_name': member.first_name + ' ' + member.last_name} for member in
        #            team.mteam.all()}
        members = {'count': team.mteam.count()}
        return JsonResponse(members)


@csrf_exempt
@login_required(login_url='login')
def remove_member(request, pk):
    if request.method == "DELETE":
        team = request.user.team
        print("delete memeber")
        member = get_object_or_404(TeamUser, pk=pk)
        member.delete()
        return JsonResponse({"member_count": team.mteam.count(), 'data': 'کاربر با موفقیت حذف شد'})


@login_required(login_url='login')
def get_member(request, pk):
    if request.method == "GET":
        print('get member')
        member = get_object_or_404(TeamUser, pk=pk)
        return JsonResponse(
            {"id": member.id, "first_name": member.first_name, "last_name": member.last_name,
             "file_name": member.file_resume.name.split('/')[-1]})


@csrf_exempt
@login_required(login_url='login')
def team_user_update(request, pk):
    if request.method == "POST":
        print("update member")
        member = get_object_or_404(TeamUser, pk=pk)
        member_form = MemberTeamForm(request.POST or None, request.FILES, instance=member)
        if member_form.is_valid():
            member_form.save()
            return JsonResponse({"id": member.id, "first_name": member.first_name, "last_name": member.last_name, })
        else:
            return HttpResponseBadRequest('اطلاعات وارد شده صحیح نمی باشد')


@csrf_exempt
@login_required(login_url='accounts:login')
def send_code(request):
    if request.method == 'POST':
        print(request.FILES)
        team = request.user.team
        form = CodeForm(request.FILES)
        if form.is_valid():
            team.code = form.cleaned_data['code']
            team.save()
    print(team.code)
    return JsonResponse({"code_name": team.code.name})
