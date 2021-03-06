from rest_framework import serializers
from auctions.models import *


""" class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('author', 'title', 'date', 'excerpt') """


""" class BannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('author', 'title', 'excerpt', 'description', 'created_at', 'views', 'slug') """

class FlashNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('author', 'title', 'slug', 'date', 'views', 'excerpt') 


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('author', 'title', 'slug', 'date', 'views', 'excerpt', 'p1', 'p2', 'p3', 'p4', 'category', 'author_username', 'image1_link') 