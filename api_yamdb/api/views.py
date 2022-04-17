from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets 
from rest_framework import filters
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Category, Genre, Title, Review, Rating 
from .serializers import UserSerializer, CategorySerializer,GenreSerializer, TitleSerializer, ReviewSerializer, RatingSerializer


class UserViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer 
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year') 

class RiviewViewSet(viewsets.ModelViewSet):
    pass


class RatingViewSet(viewsets.ModelViewSet):
    pass