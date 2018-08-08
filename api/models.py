from django.contrib.auth.models import Group, User
from django.db import models


class Review(models.Model):
    """A review made by a user."""
    RATING_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))

    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default=RATING_CHOICES[0][0])
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10_000)
    ip_address = models.GenericIPAddressField()
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=100)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
