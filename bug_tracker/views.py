from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from bug_tracker.forms import SignUpForm, LoginForm, NewTicketForm, UpdateTicket, CompletedTicket, InvalidTicket
from custom_user.models import CustomUser
from tracker_ticket.models import TrackerTicket


@login_required
def home(request):
    html = 'home.html'
    data = TrackerTicket.objects.all().order_by("-ticket_status")
    return render(request, html, {'data': data})


@login_required
def ticket_detail(request, id):
    html = 'ticket_detail.html'
    data = TrackerTicket.objects.get(id=id)
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/home/'))


@staff_member_required
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


@login_required
def newticket(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = NewTicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            TrackerTicket.objects.create(
                title=data['title'],
                description=data['description'],
                user_name=request.user
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = NewTicketForm()

    return render(request, html, {'form': form})


@login_required
def updateticket(request, id):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = UpdateTicket(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            TrackerTicket.objects.filter(id=id).update(
                ticket_status='In Progress',
                assigned_user=data['assigned_user']
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UpdateTicket()

    return render(request, html, {'form': form})


@login_required
def completed_ticket(request, id):
    trackerTicket = TrackerTicket.objects.get(id=id)
    trackerTicket.assigned_user = None
    trackerTicket.completed_user = request.user
    trackerTicket.ticket_status = 'Complete'
    trackerTicket.save()
    return HttpResponseRedirect(reverse('home'))


@login_required
def invalid_ticket(request, id):

    trackerTicket = TrackerTicket.objects.get(id=id)
    trackerTicket.assigned_user = None
    trackerTicket.completed_user = None
    trackerTicket.ticket_status = 'Invalid'
    trackerTicket.save()
    return HttpResponseRedirect(reverse('home'))


@login_required
def userpage(request, id):
    html = 'userPage.html'
    user = CustomUser.objects.get(id=id)
    filed = TrackerTicket.objects.filter(user_name=user)
    assigned = TrackerTicket.objects.filter(assigned_user=user)
    completed = TrackerTicket.objects.filter(completed_user=user)
    return render(request, html, {'users': user, 'files': filed, 'assigned': assigned, 'completed': completed})
