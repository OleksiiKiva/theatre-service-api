from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import Genre

GENRE_URL = "/api/theatre/genres/"


class GenreViewSetTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="adminPassword",
        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testPassword"
        )
        content_type = ContentType.objects.get_for_model(Genre)
        permission, created = Permission.objects.get_or_create(
            codename="can_create_genre",
            name="Can Create Genre",
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.admin.user_permissions.add(permission)

        self.client.force_authenticate(user=self.user)

    def test_list_genres(self):
        response = self.client.get(GENRE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), Genre.objects.count())

    def test_create_genre(self):
        data = {"name": "Vaudeville"}
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(GENRE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.get(name="Vaudeville").name, "Vaudeville")
