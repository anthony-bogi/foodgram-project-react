from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import OurIngredientSerializer
from .models import Ingredient


class OurIngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = OurIngredientSerializer
    permission_classes = []
