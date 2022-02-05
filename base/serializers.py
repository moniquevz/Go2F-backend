from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .models import Product
from .models import Article
from .models import Template
from .models import Event
from .models import ExclusiveContent
from .models import Post
from .models import Comment
from .models import Profile
from django.core.mail import send_mail

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = User
        fields = ['_id', 'username', 'email', 'first_name', 'last_name', 'isAdmin', 'is_active']
        #fields = '__all__'

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'first_name', 'last_name', 'isAdmin', 'token','is_active']
        #fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)


class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Article
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Template
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Event
        fields = '__all__'


class ExclusiveContentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ExclusiveContent
        fields = '__all__'


# Use for user data in posts
class PostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'f_name',
            'l_name',
            'profile_image',
            'title'
        ]


# Use for profile pages
class ProfileSerializer(serializers.ModelSerializer):
    # To access fields that are not contained in profile model
    is_following = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'f_name',
            'l_name',
            '_id',
            'profile_image',
            'cover_image',
            'country',
            'city',
            'website_url',
            'title',
            'bio',
            'linkedin',
            'instagram',
            'twitter',
            'github',
            'dribble',
            'behance',
            'followers',
            "is_following",
            'follower_count',
            'following_count'
        ]

    # Get methods required for serializer method fields
    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get__id(self, obj):
        return obj.user.pk

    def get_is_following(self, obj):
        # request??
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following


MAX_POST_LENGTH = 3000
POST_ACTION_OPTIONS = ["like", "unlike", "repost"]


# To create new posts or edit existing posts
class PostCreateSerializer(serializers.ModelSerializer):
    user = PostProfileSerializer(source='user.profile', read_only=True)
    # Get likes as a read-only value (used to show number of likes in render)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['_id', 'user', 'title', 'description', 'likes', 'created']

    # Returns likes as an integer
    def get_likes(self, obj):
        return obj.likes.count()

    # Validates that max_length has not been exceeded
    def validate_description(self, value):
        if len(value) > MAX_POST_LENGTH:
            raise serializers.ValidationError("This post is too long")
        return value


# To like/unlike(/repost?)
class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()   # "Like" -> "like"
        if not value in POST_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for posts.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['_id', 'user', 'detail', 'created', 'likes']


# To display existing posts in read only format
class PostSerializer(serializers.ModelSerializer):
    user = PostProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['_id', 'user', 'title', 'description', 'likes', 'comments', 'created']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'



class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields =['email']

    

class SetNewPasswordSerializer(serializers.Serializer):
    #Please do error checking for password on the front end form
    password = serializers.CharField(max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)
    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

