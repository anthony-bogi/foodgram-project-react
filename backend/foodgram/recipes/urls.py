from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

app_name = 'recipes'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/download_shopping_cart/',
         RecipeViewSet.as_view({'get': 'download_shopping_list'}),
         name='download_shopping_list'),
    path('', include(router.urls)),
    path('recipes/<int:pk>/favorite/',
         RecipeViewSet.as_view({'post': 'create_favorite',
                                'delete': 'delete_favorite'}),
         name='create_delete_favorite'),
    path('recipes/<int:pk>/shopping_cart/',
         RecipeViewSet.as_view({'post': 'create_shopping_list',
                                'delete': 'delete_shopping_list'}),
         name='create_delete_shopping_list'),
]
