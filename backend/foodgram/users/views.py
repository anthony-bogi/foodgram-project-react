from rest_framework import status, permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from .serializers import (
    OurUserCreateSerializer,
    OurUserSerializer,
    OurPasswordReentrySerializer,
    OurSubscriptionSerializer
)
from .models import User, Subscribe


class OurUserCreateViewSet(viewsets.ModelViewSet):
    """
    Наш ViewSet для регистрации анонимного пользователя.
    Показ существующих пользователей.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    # serializer_class = OurUserCreateSerializer
    def get_serializer_class(self):
        if self.action == 'create':
            return OurUserCreateSerializer
        return OurUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OurUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Наш ViewSet для работы с пользователем и его подписками."""

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = OurUserCreateSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return OurUserCreateSerializer
    #     return OurUserSerializer
    
    # pagination_class = PageNumberPagination

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     paginator = PageNumberPagination()
    #     paginator.page_size = 6
    #     paginated_queryset = paginator.paginate_queryset(queryset, request)
    #     serializer = OurUserSerializer(paginated_queryset, many=True, context={'request': request})
    #     return paginator.get_paginated_response(serializer.data)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribers__user=user)
        # subscriptions = Subscribe.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        paginated_subscriptions = paginator.paginate_queryset(subscriptions, request)
        serializer = OurSubscriptionSerializer(
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
        subscription = Subscribe.objects.filter(
            user=request.user, author=author)
        
        if request.method == 'DELETE':
            if not subscription:
                if author != request.user:
                    return Response(
                        {'errors':'Невозможно удалить несуществующую подписку.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {'errors': 'Невозможно отписаться от самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if subscription:
            return Response(
                {'errors': 'Вы уже подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if author == request.user:
            return Response(
                {'errors': 'Невозможно подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Subscribe.objects.create(user=request.user, author=author)
        serializer = OurSubscriptionSerializer(
            author,
            context={
                'request': request
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def get(self, request, pk=None):
        user = self.get_object()
        serializer = OurUserSerializer(
            user,
            context={
                'request': request
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = OurUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get']
    )
    def me(self, request):
        user = request.user
        serializer = OurUserSerializer(user)
        return Response(serializer.data)


class OurChangePasswordViewSet(viewsets.ViewSet):
    """Наш ViewSet для смены пароля пользователем."""
    permission_classes = (permissions.IsAuthenticated,)

    def set_password(self, request):
        serializer = OurPasswordReentrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'current_password': 'Неверный пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_password = serializer.validated_data['new_password']
        if user.check_password(new_password):
            return Response(
                {'new_password': 'Новый пароль не может совпадать с текущим паролем.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
