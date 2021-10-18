from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer


from base.models import Post

from base.serializers import PostCreateSerializer, PostActionSerializer, PostSerializer

from rest_framework import status

# @api_view(['GET'])
# def getPosts(request):
#     posts = Post.objects.all()
#     serializer = PostCreateSerializer(posts, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def getPost(request, pk):
#     post = Post.objects.get(_id=pk)
#     serializer = PostCreateSerializer(post, many = False)
#     return Response(serializer.data)

@api_view(['GET', 'POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def post_detail_view(request, pk, *args, **kwargs):
    qs = Post.objects.filter(_id=pk)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete_view(request, tweet_id, *args, **kwargs):
    qs = Post.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this post."}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Post removed."}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, repost
    '''
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get("_id")
        action = data.get("action")
        title = data.get("title")
        description = data.get("description")
        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "repost":
            new_post = Post.objects.create(
                    user=request.user,
                    parent=obj,
                    )
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=201)
    return Response({}, status=200)





@api_view(['GET'])
def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.filter(user__username__iexact=username)
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)