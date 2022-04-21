from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
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
    filter_backends = (SearchFilter,)
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
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
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


class ReviewViewSet(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, title_id):
        reviews = Review.objects.filter(title_id=title_id)

        results = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(results, many=True)
        paginated_data = self.get_paginated_response(serializer.data)

        return Response(data=paginated_data.data)

    def post(self, request, title_id):
        if not request.data or not int(request.data['score']) in range(1, 10):
            return Response(status=HTTP_400_BAD_REQUEST)
        title = get_object_or_404(Title, id=title_id)
        request.POST._mutable = True
        data = request.data
        data['author'] = request.user.id
        data['title'] = title_id
        request.POST._mutable = False
        serializer = ReviewSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save(
                    author=request.user,
                    title_id=title_id
                )
                return Response(data=serializer.data, status=HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ReviewSingleView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
