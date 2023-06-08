from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OurUserViewSet


router = DefaultRouter()
router.register(r'users', OurUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
