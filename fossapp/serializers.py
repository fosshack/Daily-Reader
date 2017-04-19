from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ('id', 'upvotes', 'downvotes', 'is_voted', 'image')