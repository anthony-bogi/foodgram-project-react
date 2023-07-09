from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.constants import PAGINATION_SIZE

from .models import Subscribe, User
from .serializers import (ModifiedUserCreateSerializer, ModifiedUserSerializer,
                          PasswordReentrySerializer, SubscriptionSerializer)


class UserCreateViewSet(viewsets.ModelViewSet):
    """
    Наш ViewSet для регистрации анонимного пользователя.
    Показ существующих пользователей.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    pagination_class.page_size = PAGINATION_SIZE

    def get_serializer_class(self):
        if self.action == 'create':
            return ModifiedUserCreateSerializer
        return ModifiedUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # noqa
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.GenericViewSet):
    """Наш ViewSet для работы с пользователем и его подписками."""

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ModifiedUserCreateSerializer

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribers__user=user)
        paginator = PageNumberPagination()
        paginator.page_size = PAGINATION_SIZE
        paginated_subscriptions = paginator.paginate_queryset(
            subscriptions,
            request
        )
        serializer = SubscriptionSerializer(
            paginated_subscriptions,
            many=True,
            context={
                'request': request
            }
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        serializer = SubscriptionSerializer(
            author,
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        if serializer.is_valid():
            if request.method == 'DELETE':
                subscription = Subscribe.objects.filter(
                    user=request.user,
                    author=author
                )
                if not subscription.exists():
                    return Response(
                        {'errors':
                         ' Невозможно удалить несуществующую подписку.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer.save()
            Subscribe.objects.create(user=request.user, author=author)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def get(self, request, pk=None):
        user = self.get_object()
        serializer = ModifiedUserSerializer(
            user,
            context={
                'request': request
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ModifiedUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get']
    )
    def me(self, request):
        user = request.user
        serializer = ModifiedUserSerializer(user)
        return Response(serializer.data)


class ChangePasswordViewSet(viewsets.ViewSet):
    """Наш ViewSet для смены пароля пользователем."""
    permission_classes = (permissions.IsAuthenticated,)

    def set_password(self, request):
        serializer = PasswordReentrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(
            serializer.validated_data['current_password']
        ):
            return Response(
                {'current_password': 'Неверный пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_password = serializer.validated_data['new_password']
        if user.check_password(new_password):
            return Response(
                {
                    'new_password':
                    ' Новый пароль не может совпадать с текущим паролем.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
