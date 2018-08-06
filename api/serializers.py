from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
