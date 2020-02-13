from django.db import models
from django.utils import timezone
from custom_user.models import CustomUser


class TrackerTicket(models.Model):
    New = 'New'
    In_Progress = 'In Progress'
    Done = 'Done'
    Invalid = 'Invalid'

    TICKET_STATUS_CHOICES = [
        (New, 'New'),
        (In_Progress, 'In Progress'),
        (Done, 'Done'),
        (Invalid, 'Invalid')
    ]

    title = models.CharField(max_length=30)
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user_name = models.ForeignKey(
        CustomUser, related_name='ticket_user_name', on_delete=models.CASCADE, null=True)
    assigned_user = models.ForeignKey(
        CustomUser, related_name='ticket_assigned_user', on_delete=models.CASCADE, null=True)
    completed_user = models.ForeignKey(
        CustomUser, related_name='ticket_completed_user', on_delete=models.CASCADE, null=True)
    ticket_status = models.CharField(
        max_length=15, choices=TICKET_STATUS_CHOICES, default=New)
