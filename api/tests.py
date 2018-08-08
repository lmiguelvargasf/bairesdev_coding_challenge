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
    def test_create_review(self):
        """
        Ensure we can create a new review object.
        """
        url = reverse('review-list')
        rating = '3'
        title = 'This is a title'
        summary = 'This is a summary...'
        company = 'Company Inc'
        data = {'rating': rating,
                'title': title,
                'summary': summary,
                'company': company}
        PASSWORD = 'password'
        reviewer = User.objects.create_user(username='testuser',
                                            password=PASSWORD,
                                            email='email@example.com')
        self.client.login(username=reviewer.username, password=PASSWORD)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, '3')
        self.assertEqual(Review.objects.get().summary, summary)
        self.assertEqual(Review.objects.get().company, company)
        self.assertEqual(Review.objects.get().reviewer, reviewer)


    def test_unauthorized(self):
        """
        Ensure we can create a new review object.
        """
        url = reverse('review-list')
        rating = '3'
        title = 'This is a title'
        summary = 'This is a summary...'
        company = 'Company Inc'
        data = {'rating': rating,
                'title': title,
                'summary': summary,
                'company': company}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        PASSWORD = 'password'
        reviewer = User.objects.create_user(username='testuser',
                                            password=PASSWORD,
                                            email='email@example.com')
        another_reviewer = User.objects.create_user(username='another_test_user',
                                                    password=PASSWORD,
                                                    email='another@example.com')
        url = reverse('review-list')
        rating = '3'
        title = 'This is a title'
        summary = 'This is a summary...'
        ip_address = '127.0.0.1'
        submission_date = timezone.now()
        company = 'Company Inc'
        reviewer_review = Review.objects.create(rating=rating,
                                                title=title,
                                                summary=summary,
                                                ip_address=ip_address,
                                                submission_date=submission_date,
                                                company=company,
                                                reviewer=reviewer)
        another_review = Review.objects.create(rating=rating,
                                               title=title,
                                               summary=summary,
                                               ip_address=ip_address,
                                               submission_date=submission_date,
                                               company=company,
                                               reviewer=another_reviewer)

        self.client.login(username=reviewer.username, password=PASSWORD)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(len(response.data), 1)
