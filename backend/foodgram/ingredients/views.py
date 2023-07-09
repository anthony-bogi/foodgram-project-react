from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = []
