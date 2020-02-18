from django import forms
from django.contrib.auth.forms import UserCreationForm

from custom_user.models import CustomUser
from tracker_ticket.models import TrackerTicket


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'age'
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = TrackerTicket
        fields = [
            'title',
            'description'
        ]


class UpdateTicket(forms.ModelForm):
    class Meta:
        model = TrackerTicket
        fields = [
            'assigned_user'
        ]
