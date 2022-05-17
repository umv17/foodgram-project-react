from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )
        model = User
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'is_subscribed'
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, following=obj).exists()


class RecipeForFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ListFollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.following)
        serializer = RecipeForFollowSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.id).count()
