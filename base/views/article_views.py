from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer


from base.models import Article
from base.articles import articles
from base.serializers import ArticleSerializer

from rest_framework import status

@api_view(['GET'])
def getArticles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getArticle(request, pk):
    article = Article.objects.get(_id=pk)
    serializer = ArticleSerializer(article, many = False)
    return Response(serializer.data)