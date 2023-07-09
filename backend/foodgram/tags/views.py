from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
