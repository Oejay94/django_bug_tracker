from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from bug_tracker.forms import SignUpForm, LoginForm
from custom_user.models import CustomUser


@login_required
def home(request):
    html = 'home.html'
    data = CustomUser.objects.all()
    return render(request, html, {'data': data})


def login_view(request):
    html = 'generic_form.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()

    return render(request, html, {'form': form})


@login_required
def signup(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = CustomUser.objects.create_user(
                data['username'], data['first_name'], data['password1']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(request, html, {'form': form})
