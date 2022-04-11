from rest_framework import serializers
from auctions.models import *
from auctions.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('author', 'title', 'date', 'excerpt')


""" class BannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('author', 'title', 'excerpt', 'description', 'created_at', 'views', 'slug') """

class FlashNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('author', 'title', 'date', 'views', 'excerpt') 