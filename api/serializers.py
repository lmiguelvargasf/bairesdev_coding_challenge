from rest_framework import serializers

from .models import Review


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        exclude = ('submission_date', 'ip_address', 'reviewer', 'url')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        ip_address = get_client_ip(request)
        review = Review.objects.create(reviewer=user,
                                       ip_address=ip_address,
                                       **validated_data)

        return review
