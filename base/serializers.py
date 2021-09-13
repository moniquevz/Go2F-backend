from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from .models import Article
from .models import Template


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