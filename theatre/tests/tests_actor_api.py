from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import Actor

ACTOR_URL = "/api/theatre/actors/"


class ActorViewSetTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="adminPassword",
        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testPassword"
        )
        content_type = ContentType.objects.get_for_model(Actor)
        permission, created = Permission.objects.get_or_create(
            codename="can_create_actor",
            name="Can Create Actor",
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.admin.user_permissions.add(permission)

        self.client.force_authenticate(user=self.user)

    def test_list_actors(self):
        response = self.client.get(ACTOR_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), Actor.objects.count())

    def test_create_actor(self):
        data = {"first_name": "Jude", "last_name": "Law"}
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(ACTOR_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actor.objects.get(first_name="Jude").first_name, "Jude")
        self.assertEqual(Actor.objects.get(last_name="Law").last_name, "Law")
