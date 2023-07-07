from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (OurChangePasswordViewSet, OurUserCreateViewSet,
                    OurUserViewSet)

app_name = 'users'

router = DefaultRouter()
router.register(r'users', OurUserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/',
         OurChangePasswordViewSet.as_view({'post': 'set_password'}),
         name='change-password'
         ),
    path('users/',
         OurUserCreateViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='create-user'
         ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
