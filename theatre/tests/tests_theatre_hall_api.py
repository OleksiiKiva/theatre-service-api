from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import TheatreHall

THEATRE_HALL_URL = "/api/theatre/theatrehalls/"


class TheatreHallViewSetTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="adminPassword",
        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testPassword"
        )
        content_type = ContentType.objects.get_for_model(TheatreHall)
        permission, created = Permission.objects.get_or_create(
            codename="can_create_theatrehall",
            name="Can Create Theatre Hall",
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.admin.user_permissions.add(permission)

        self.client.force_authenticate(user=self.user)

    def test_list_theatre_halls(self):
        response = self.client.get(THEATRE_HALL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), TheatreHall.objects.count())

    def test_create_theatre_hall(self):
        data = {"name": "Piccolo Teatro di Milano", "rows": 40, "seats_in_row": 50}
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(THEATRE_HALL_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            TheatreHall.objects.get(
                name="Piccolo Teatro di Milano").name,
            "Piccolo Teatro di Milano"
        )
        self.assertEqual(TheatreHall.objects.get(rows=40).rows, 40)
        self.assertEqual(TheatreHall.objects.get(seats_in_row=50).seats_in_row, 50)
