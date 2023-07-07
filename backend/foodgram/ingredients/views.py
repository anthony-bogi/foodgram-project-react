from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient
from .serializers import OurIngredientSerializer


class OurIngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = OurIngredientSerializer
    permission_classes = []
