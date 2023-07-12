import os
from collections import defaultdict
from io import BytesIO

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .constants import (DELTA_Y_COORD_PAGE, FONT_SIZE, LIST_Y_COORD_PAGE,
                        PAGINATION_SIZE, START_X_COORD_PAGE,
                        START_Y_COORD_PAGE)
from .exceptions import MissingFontError
from .filters import RecipeFilter
from .models import Favorites, Ingredients, Recipe, ShoppingList
from .permissions import IsRecipeAuthorOrReadOnly
from .serializers import (FavoritesSLRecipeSerializer,
                          RecipeCreateUpdateSerializer, RecipeSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """Наш ViewSet для работы с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    pagination_class.page_size = PAGINATION_SIZE
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            recipe_id = self.kwargs.get('pk')
            if not Recipe.objects.filter(id=recipe_id).exists():
                self.permission_classes = [permissions.IsAuthenticated]
            else:
                self.permission_classes = [IsRecipeAuthorOrReadOnly]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return super().get_queryset()

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def create_favorite(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        favorite, created = Favorites.objects.get_or_create(user=user,
                                                            recipe=recipe)
        if not created:
            return Response(
                {'error': 'Рецепт уже добавлен в избранное.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FavoritesSLRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def delete_favorite(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        favorites = Favorites.objects.filter(user=user, recipe=recipe)
        if not favorites.exists():
            return Response(
                {'error': 'Рецепт не найден в избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorites.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def create_shopping_list(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        shopping_list, created = ShoppingList.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        if not created:
            return Response(
                {'error': 'Рецепт уже добавлен в список покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FavoritesSLRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def delete_shopping_list(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        shopping_list = ShoppingList.objects.filter(user=user, recipe=recipe)
        if not shopping_list.exists():
            return Response(
                {'error': 'Рецепт не найден в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_list(self, request):
        user = self.get_serializer_context()['request'].user
        shopping_list = ShoppingList.objects.filter(user=user)
        if not shopping_list.exists():
            return HttpResponse('Список покупок пуст.')
        ingredients = (Ingredients.objects
                       .filter(recipe__shopping_list__in=shopping_list)
                       .values('ingredient__name',
                               'amount',
                               'ingredient__measurement_unit'))
        ingredient_totals = defaultdict(float)

        for ingredient in ingredients:
            ingredient_name = ingredient['ingredient__name']
            ingredient_quantity = ingredient['amount']
            ingredient_unit = ingredient['ingredient__measurement_unit']
            ingredient_totals[ingredient_name] += ingredient_quantity

        pdf_buffer = BytesIO()

        p = canvas.Canvas(pdf_buffer, pagesize=letter)

        try:
            if os.path.exists('./fonts/ArialRegular.ttf'):
                pdfmetrics.registerFont(TTFont(
                    'Arial',
                    './fonts/ArialRegular.ttf')
                )
                p.setFont('Arial', FONT_SIZE)
            else:
                raise MissingFontError
        except MissingFontError:
            error = MissingFontError()
            return error.generate_txt_shopping_list(ingredient_totals)

        p.drawString(START_X_COORD_PAGE, START_Y_COORD_PAGE, 'Список покупок')

        y = LIST_Y_COORD_PAGE

        for ingredient_name, ingredient_quantity in (
            ingredient_totals.items()
        ):
            ingredient_unit = (
                Ingredients.objects.filter(ingredient__name=ingredient_name)
                .first()
                .ingredient.measurement_unit
            )
            p.drawString(
                START_X_COORD_PAGE,
                y,
                "{}: {} {}".format(ingredient_name,
                                   ingredient_quantity,
                                   ingredient_unit)
            )
            y -= DELTA_Y_COORD_PAGE

        p.showPage()
        p.save()

        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.pdf"'
        )

        return response
