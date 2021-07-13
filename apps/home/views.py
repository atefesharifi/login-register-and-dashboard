from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect

from .forms import *
from .models.rules import Rules
from .models.sponsor import Sponsor


def home(request):
    sponsor = Sponsor.objects.all()
    try:
        rules = Rules.objects.all()[0]
        return render(request, 'home/home.html', {'sponsor': sponsor, 'rules': rules})

    except:
        return render(request, 'home/home.html', {'sponsor': sponsor})


def download(request):
    obj = Rules.objects.all()[0]
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


@login_required(login_url='accounts:login')
def sendcode(request):
    if request.method == 'POST':
        form = CodeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data["code"]
            user = request.user
            user.code = data
            user.save()
            messages.success(request, 'کد شما ثبت شد', 'success')
            return redirect('home:home')
    else:
        form = CodeForm()
    return render(request, 'home/sendcode.html', {'form': form})
