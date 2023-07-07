from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tag
from .serializers import OurTagSerializer


class OurTagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для вывода списка доступных тегов."""
    queryset = Tag.objects.all()
    serializer_class = OurTagSerializer
    permission_classes = []
