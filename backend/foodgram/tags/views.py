from rest_framework.viewsets import ReadOnlyModelViewSet
# from rest_framework.pagination import PageNumberPagination

from .serializers import OurTagSerializer
from .models import Tag


class OurTagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных тегов."""
    queryset = Tag.objects.all()
    serializer_class = OurTagSerializer
    permission_classes = []
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 100
