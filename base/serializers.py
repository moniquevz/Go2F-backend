from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from .models import Article
from .models import Template
from .models import Event
from .models import ExclusiveContent
from .models import Post
from .models import Comment

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = User
        fields = ['_id', 'username', 'email', 'first_name', 'last_name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'first_name', 'last_name', 'isAdmin', 'token']

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


class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment
        fields = '__all__'