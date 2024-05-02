from django.shortcuts import render
from rest_framework import viewsets

from theatre.models import Genre, Actor, Play
from theatre.serializers import GenreSerializer, ActorSerializer, PlaySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects
    serializer_class = ActorSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects
    serializer_class = PlaySerializer
