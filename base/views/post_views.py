from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer


from base.models import Post

from base.serializers import PostSerializer

from rest_framework import status

@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(_id=pk)
    serializer = PostSerializer(post, many = False)
    return Response(serializer.data)