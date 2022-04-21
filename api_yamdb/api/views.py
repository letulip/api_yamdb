from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .mixins import ModelMixinSet
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer

)
from .permissions import IsOwnerModerAdminOrReadOnly, IsAdminOrReadOnly


class CategoryViewSet(ModelMixinSet):
    permission_classes = [

        IsAuthenticatedOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [

        IsAuthenticatedOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(APIView):
    #queryset = Review.objects.all()
    #serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def get_queryset(self, title_id):
    #    title_id = self.kwargs.get('title_id')
    #    queryset = Review.objects.filter(title_id=title_id)
    #    return queryset

    def get(self, request, title_id):
        reviews = Review.objects.filter(title_id=title_id)
        #reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)

    def post(self, request, title_id):
#        instance = Review.objects.filter(
#            author=self.request.user,
#            title_id=self.kwargs.get('title_id')
#        )
#        if not instance.exists():
#            
#        else: 
#            return Response(
#                data=serializer.data,
#                status=HTTP_400_BAD_REQUEST
#            )
        data = request.data
        data['author'] = request.user.id
        data['title'] = title_id
        serializer = ReviewSerializer(data=data)
        # breakpoint()
        try:
            if serializer.is_valid():
                serializer.save(
                    author=request.user,
                    title_id=title_id
                )
                return Response(serializer.data, status=HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
