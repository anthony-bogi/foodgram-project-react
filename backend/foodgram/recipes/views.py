from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from collections import defaultdict
from django.http import HttpResponse
from rest_framework import status, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Recipe, Ingredients, Favorites, ShoppingList
from .serializers import (OurRecipeSerializer,
                          OurRecipeCreateSerializer,
                          OurRecipeCreateOutputSerializer,
                          OurFavoritesSLRecipeSerializer)
from ingredients.models import Ingredient


class OurRecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """Наш ViewSet для работы с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = OurRecipeSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6

    def get_permissions(self):
        if self.action in [
            'create',
            'partial_update',
            'destroy',
            'create_favorite',
            'delete_favorite',
            'create_shopping_list',
            'delete_shopping_list',
            'download_shopping_list'
        ]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def create(self, request, *args, **kwargs):
        create_serializer = OurRecipeCreateSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        author = request.user
        validated_data = create_serializer.validated_data
        validated_data['author'] = author
        ingredients_data = request.data.get('ingredients')
        recipe = create_serializer.save()
        if ingredients_data:
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                amount = ingredient_data.get('amount')
                ingredient = Ingredient.objects.get(id=ingredient_id)
                Ingredients.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
        output_serializer = OurRecipeCreateOutputSerializer(
            recipe,
            context={'request': request}
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            return Response(
                {"error": "Вы не являетесь автором этого рецепта."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = OurRecipeCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        output_serializer = OurRecipeCreateOutputSerializer(
            instance,
            context={'request': request}
        )
        return Response(output_serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            return Response({"error": "Вы не являетесь автором этого рецепта."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def create_favorite(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        recipe = self.get_object()
        user = request.user
        favorite, created = Favorites.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            return Response(
                {"error": "Рецепт уже добавлен в избранное."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = OurFavoritesSLRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete_favorite(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        recipe = self.get_object()
        user = request.user
        favorites = Favorites.objects.filter(user=user, recipe=recipe)
        if not favorites.exists():
            return Response(
                {"error": "Рецепт не найден в избранном."},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorites.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def create_shopping_list(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        shopping_list, created = ShoppingList.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            return Response(
                {"error": "Рецепт уже добавлен в список покупок."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = OurFavoritesSLRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete_shopping_list(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        shopping_list = ShoppingList.objects.filter(user=user, recipe=recipe)
        if not shopping_list.exists():
            return Response(
                {"error": "Рецепт не найден в списке покупок."},
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def download_shopping_list(self, request):
        user = self.get_serializer_context()['request'].user
        shopping_list = ShoppingList.objects.filter(user=user)
        if not shopping_list.exists():
            return HttpResponse("Список покупок пуст.")
        ingredients = Ingredients.objects.filter(recipe__shopping_list__in=shopping_list).values('ingredient__name', 'amount', 'ingredient__measurement_unit')
        ingredient_totals = defaultdict(float)
                
        for ingredient in ingredients:
            ingredient_name = ingredient['ingredient__name']
            ingredient_quantity = ingredient['amount']
            ingredient_unit = ingredient['ingredient__measurement_unit']
            ingredient_totals[ingredient_name] += ingredient_quantity
        
        pdf_buffer = BytesIO()

        p = canvas.Canvas(pdf_buffer, pagesize=letter)

        try:
            pdfmetrics.registerFont(TTFont('Arial', 'C:/WINDOWS/FONTS/ARIAL.ttf'))
            p.setFont("Arial", 12)
        except:
            p.setFont("Helvetica", 12)
        
        p.drawString(100, 750, "Список покупок")

        y = 700

        for ingredient_name, ingredient_quantity in ingredient_totals.items():
            ingredient_unit = Ingredients.objects.filter(ingredient__name=ingredient_name).first().ingredient.measurement_unit
            p.drawString(100, y, f"{ingredient_name}: {ingredient_quantity} {ingredient_unit}")
            y -= 20
        
        p.showPage()
        p.save()

        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.pdf"'

        return response
