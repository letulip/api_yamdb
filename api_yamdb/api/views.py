from django.shortcuts import render

from rest_framework import viewsets 
from rest_framework import filters

from .models import User, Category, Genre, Title, Review, Rating 
from .serializers import UserSerializer, CategorySerializer,GenreSerializer, TitleSerializer, ReviewSerializer, RatingSerializer


class UserViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer 


class RiviewViewSet(viewsets.ModelViewSet):
    pass


class RatingViewSet(viewsets.ModelViewSet):
    pass

