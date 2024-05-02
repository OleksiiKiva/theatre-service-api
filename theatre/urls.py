from django.urls import path, include
from rest_framework import routers

from theatre.views import GenreViewSet, ActorViewSet, PlayViewSet, TheatreHallViewSet

app_name = "theatre"

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("plays", PlayViewSet)
router.register("theatrehalls", TheatreHallViewSet)

urlpatterns = [path("", include(router.urls)), ]
