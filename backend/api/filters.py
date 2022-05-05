from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class CustomRecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_favorite',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shop_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'tags',
            'is_in_shopping_cart',
        )

    def get_favorite(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            queryset = queryset.filter(recipe_favorite__user=self.request.user)
        return queryset

    def get_shop_cart(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            queryset = queryset.filter(list_recipe__user=self.request.user)
        return queryset


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
