from django.shortcuts import render
from rest_framework import viewsets

from theatre.models import Genre
from theatre.serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects
    serializer_class = GenreSerializer
