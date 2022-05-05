from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShopCart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination
from api.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                             IngredientSerializer, ListRecipeSerializer,
                             ShopCartSerializer, TagSerializer)

from .filters import CustomRecipeFilter, IngredientFilter
from .mixins import CreateOrListViewSet
from .permissions import IsAuthorOrAdminOrReadOnly


class TagViewSet(CreateOrListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(CreateOrListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthorOrAdminOrReadOnly,
    ]
    serializer_class = CreateRecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return CreateRecipeSerializer
        return ListRecipeSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def shopcart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user        
        if request.method == 'POST':
            if ShopCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Этот рецепт уже добавлен в корзину'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shop_cart = ShopCart.objects.create(user=user, recipe=recipe)
            serializer = ShopCartSerializer(
                shop_cart, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            delete_shop_cart = ShopCart.objects.filter(
                user=user, recipe=recipe)
            if delete_shop_cart.exists():
                delete_shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        method = request.method
        if method == 'POST':
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(
                favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def shop_cart(self, request):
        user = request.user
        all_count_ingredients = (
            IngredientAmount.objects.filter(
                recipe__list_recipe__user = user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        shop_list = {}
        for ingredient in all_count_ingredients:
            amount = ingredient['amount']
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            shop_list[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit}
        sub_title = f'{timezone.now().date()}'
        response = HttpResponse(content_type='application/pdf')
        content_disposition = f'attachment; filename="shopping-list.pdf"'
        response['Content-Disposition'] = content_disposition
        pdf = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont
            (
            'FreeSans',
            'media/fonts/FreeSans.ttf')
            )
        pdf.setFont('FreeSans', 24)
        pdf.drawCentredString(300, 770, 'Список покупок')
        pdf.setFont('FreeSans', 16)
        pdf.drawCentredString(290, 720, sub_title)
        pdf.line(30, 710, 565, 710)
        height = 670
        for name, data in shop_list.items():
            pdf.drawString(
                50,
                height,
                f"{name} - {data['amount']} {data['measurement_unit']}"
            )
            height -= 25
        pdf.showPage()
        pdf.save()
        return response
