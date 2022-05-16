from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Наименование'
    )
    color = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='tags_recipe',
        verbose_name='Tag'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_recipe',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients_recipe',
        verbose_name='Инградиенты рецепта'
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Наименование',
    )
    image = models.ImageField(
        upload_to='media/',
        verbose_name='Картинка',
        blank=True,
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)],
        blank=False,
        null=False,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления рецепта',
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shop',
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount', validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Amount'
        verbose_name_plural = 'Amounts'

    def __str__(self):
        return f'{self.ingredient}: {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Favorite recipe'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.recipe}'


class ShopCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='list_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Shoping cart'
        verbose_name_plural = 'Shoping carts'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_shop_cart'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.recipe}'
