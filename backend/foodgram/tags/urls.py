from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OurTagViewSet


app_name = 'tags'

router = DefaultRouter()
router.register(r'tags', OurTagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
