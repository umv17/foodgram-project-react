from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShopCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('id', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)


@admin.register(ShopCart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)


@admin.register(IngredientAmount)
class IngredientAmount(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe')
    search_fields = ('id', 'ingredient', 'recipe')
    list_filter = ('id', 'ingredient', 'recipe')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', )
    list_display_links = ('id', 'name', )
    list_filter = ('name', 'author', 'tags')

    def count_favorite(self, obj):
        user = self.context['request'].user
        return Favorite.objects.filter(user=user, recipe=obj).count()
