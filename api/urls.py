from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
