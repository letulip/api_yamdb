from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .mixins import ModelMixinSet
from .filters import TitleFilter
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer

)
from .permissions import (
    IsOwnerModerAdminOrReadOnly,
    IsAdminOrReadOnlyIldar
)


class CategoryViewSet(ModelMixinSet):
    permission_classes = [
        IsAdminOrReadOnlyIldar,
        IsAuthenticatedOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    permission_classes = [
        IsAdminOrReadOnlyIldar,
        IsAuthenticatedOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdminOrReadOnlyIldar,
        IsAuthenticatedOrReadOnly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlePostSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnly,)

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        new_queryset = Comment.objects.filter(id=comment_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
