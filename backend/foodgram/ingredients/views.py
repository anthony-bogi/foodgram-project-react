from rest_framework.viewsets import ReadOnlyModelViewSet
# from rest_framework.pagination import PageNumberPagination

from .serializers import OurIngredientSerializer
from .models import Ingredient


class OurIngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = OurIngredientSerializer
    permission_classes = []
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 100
