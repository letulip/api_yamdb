from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN
)
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
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
    IsAdminOrReadOnlyIldar,
    IsOwnerModerAdminOrReadOnlyKonstantin,
)
from api_yamdb.settings import USER


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


class ReviewViewSet(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, title_id):
        reviews = Review.objects.filter(title_id=title_id)
        results = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(results, many=True)
        paginated_data = self.get_paginated_response(serializer.data)

        return Response(data=paginated_data.data)

    def post(self, request, title_id):
        if not request.data or int(request.data['score']) > 10 or int(request.data['score']) == 0:
            return Response(status=HTTP_400_BAD_REQUEST)
        title = get_object_or_404(Title, id=title_id)
        request.data._mutable = True
        data = request.data
        data['author'] = request.user.id
        data['title'] = title_id
        request.data._mutable = False
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

class APIReviewDetail(APIView):
    permission_classes = (IsOwnerModerAdminOrReadOnly,)
    
    def get(self, request, title_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def patch(self, request, title_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        # костыль
        if request.user != review.author:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self,request, title_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        # костыль
        if request.user.role == USER:
            return Response(status=HTTP_403_FORBIDDEN)
        review.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnlyKonstantin,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review_id=review_id)

        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        title_id = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user,
            review=review,
        )

        return Response(serializer.data, status=HTTP_200_OK)
