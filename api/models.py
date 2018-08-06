from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from star_ratings.models import Rating


class Review(models.Model):
    """A review made by a user."""
    rating = GenericRelation(Rating)
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10_000)
    ip_address = models.GenericIPAddressField()
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Group, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
