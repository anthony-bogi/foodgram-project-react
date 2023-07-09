from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChangePasswordViewSet, UserCreateViewSet, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/',
         ChangePasswordViewSet.as_view({'post': 'set_password'}),
         name='change-password'
         ),
    path('users/',
         UserCreateViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='create-user'
         ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
