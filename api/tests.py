from unittest import mock
from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Review
from .serializers import get_client_ip


@pytest.mark.django_db
def test_review_is_created():
    """Verifies that an instance of Review is created properly."""
    rating = '3'
    title = 'This is a title'
    summary = 'This is a summary...'
    ip_address = '127.0.0.1'
    submission_date = timezone.now()
    company = 'Company Inc'
    reviewer = User.objects.create_user(username='testuser',
                                        password='password',
                                        email='email@example.com')

    with mock.patch('django.utils.timezone.now', return_value=submission_date):
        review = Review.objects.create(rating=rating,
                                       title=title,
                                       summary=summary,
                                       ip_address=ip_address,
                                       submission_date=submission_date,
                                       company=company,
                                       reviewer=reviewer)

    assert isinstance(review, Review)
    assert review.rating == rating
    assert review.title == title
    assert review.summary == summary
    assert review.submission_date == submission_date
    assert review.company == company
    assert review.reviewer == reviewer


def test_get_client_ip_with_x_forwarded_for():
    """Test ip address is returned properly when request contains HTTP_X_FORWARDED_FOR"""
    ip_address = '127.0.0.1'
    request = MagicMock()
    request.META = {'HTTP_X_FORWARDED_FOR': ip_address}

    assert get_client_ip(request) == ip_address


def test_get_client_ip_without_x_forwarded_for():
    """Test ip address is returned properly when request does not contain
    HTTP_X_FORWARDED_FOR"""
    ip_address = '127.0.0.1'
    request = MagicMock()
    request.META = {'REMOTE_ADDR': ip_address}

    assert get_client_ip(request) == ip_address


class ReviewTests(APITestCase):
    PASSWORD = 'password'

    def setUp(self):
        self.url = reverse('review-list')
        self.reviewer = User.objects.create_user(username='reviewer',
                                            password=self.PASSWORD,
                                            email='reviewer@example.com')
        self.data = {'rating': '3',
                     'title': 'This is a title',
                     'summary': 'This is a summary...',
                     'company': 'Company Inc'}

    def test_create_review(self):
        """
        Ensure we can create a new review object.
        """
        self.client.login(username=self.reviewer.username, password=self.PASSWORD)
        response = self.client.post(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Review.objects.count() == 1
        assert Review.objects.get().rating == self.data['rating']
        assert Review.objects.get().title == self.data['title']
        assert Review.objects.get().summary == self.data['summary']
        assert Review.objects.get().company == self.data['company']
        assert Review.objects.get().reviewer == self.reviewer

    def test_unauthorized(self):
        """
        Ensure we can create a new review object only when user is authenticated
        """
        response = self.client.post(self.url, self.data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Review.objects.count() == 0

    def test_get(self):
        another_reviewer = User.objects.create_user(username='another_test_user',
                                                    password=self.PASSWORD,
                                                    email='another@example.com')
        ip_address = '127.0.0.1'
        submission_date = timezone.now()
        reviewer_review = Review.objects.create(ip_address=ip_address,
                                                submission_date=submission_date,
                                                reviewer=self.reviewer,
                                                **self.data)
        another_review = Review.objects.create(ip_address=ip_address,
                                               submission_date=submission_date,
                                               reviewer=another_reviewer,
                                               **self.data)

        self.client.login(username=self.reviewer.username, password=self.PASSWORD)
        response = self.client.get(self.url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert Review.objects.count() == 2
        assert len(response.data) == 1
