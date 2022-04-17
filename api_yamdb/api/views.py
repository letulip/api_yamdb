from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Review, Rating, Comment
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    RatingSerializer,
    CommentSerializer
)
from .permissions import IsOwnerModerAdminOrReadOnly, IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year') 


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
        comment_id = self.kwargs.get("comment_id")
        new_queryset = Comment.objects.filter(id=comment_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
