from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View

from bug_tracker.forms import SignUpForm, LoginForm, NewTicketForm, UpdateTicket, CompleteTicketForm, InvalidTicketForm
from custom_user.models import CustomUser
from tracker_ticket.models import TrackerTicket


@login_required
def home(request):
    html = 'home.html'
    data = TrackerTicket.objects.filter(ticket_status=TrackerTicket.New).order_by("-time")
    in_progress = TrackerTicket.objects.filter(ticket_status=TrackerTicket.In_Progress).order_by("-time")
    done = TrackerTicket.objects.filter(ticket_status=TrackerTicket.Done).order_by("-time")
    invalid = TrackerTicket.objects.filter(ticket_status=TrackerTicket.Invalid).order_by("-time")
    return render(request, html, {'data': data, 'in_progress': in_progress, 'done': done, 'invalid': invalid})


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
                assigned_user=data['assigned_user'],
                title=data['title'],
                description=data['description']
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UpdateTicket()

    return render(request, html, {'form': form})



@login_required
def completed_ticket(request, id):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = CompleteTicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            TrackerTicket.objects.filter(id=id).update(
                assigned_user=None,
                completed_user=request.user,
                ticket_status='Done',
                title=data['title'],
                description=data['description']
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = CompleteTicketForm()

    return render(request, html, {'form': form})
 

@login_required
def invalid_ticket(request, id):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = InvalidTicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            TrackerTicket.objects.filter(id=id).update(
                title=data['title'],
                description=data['description'],
                assigned_user=None,
                completed_user=None,
                ticket_status='Invalid'
            )
            return HttpResponseRedirect(reverse('home'))

    else:
        form = InvalidTicketForm()

        return render(request, html, {'form': form})

    # trackerTicket = TrackerTicket.objects.get(id=id)
    # trackerTicket.assigned_user = None
    # trackerTicket.completed_user = None
    # trackerTicket.ticket_status = 'Invalid'
    # trackerTicket.save()
    # return HttpResponseRedirect(reverse('home'))


@login_required
def userpage(request, id):
    html = 'userPage.html'
    user = CustomUser.objects.get(id=id)
    filed = TrackerTicket.objects.filter(user_name=user)
    assigned = TrackerTicket.objects.filter(assigned_user=user)
    completed = TrackerTicket.objects.filter(completed_user=user)
    return render(request, html, {'users': user, 'files': filed, 'assigned': assigned, 'completed': completed})
