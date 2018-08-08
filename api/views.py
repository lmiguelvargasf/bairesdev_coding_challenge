from rest_framework import viewsets

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)
