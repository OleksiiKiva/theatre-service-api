from django.shortcuts import render
from rest_framework import viewsets

from theatre.models import Genre, Actor, Play, TheatreHall
from theatre.serializers import GenreSerializer, ActorSerializer, PlaySerializer, TheatreHallSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects
    serializer_class = ActorSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects
    serializer_class = PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects
    serializer_class = TheatreHallSerializer
