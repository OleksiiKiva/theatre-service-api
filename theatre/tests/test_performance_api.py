from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import Performance, Play, TheatreHall

PERFORMANCE_URL = "/api/theatre/performances/"


class PerformanceViewSetTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="adminPassword",
        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testPassword"
        )
        content_type = ContentType.objects.get_for_model(Performance)
        permission, created = Permission.objects.get_or_create(
            codename="can_create_performance",
            name="Can Create Performance",
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.admin.user_permissions.add(permission)

        self.client.force_authenticate(user=self.user)
        self.play = Play.objects.create(
            title="	Hamlet",
            description="Based on the novel by William Shakespeare"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Piccolo Teatro di Milano", rows=40, seats_in_row=50
        )

    def test_list_performances(self):
        response = self.client.get(PERFORMANCE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), Performance.objects.count())

    def test_create_performance(self):
        data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2024-06-08T19:00:00",
        }
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(PERFORMANCE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Performance.objects.filter(
                play=self.play.id,
                theatre_hall=self.theatre_hall,
                show_time="2024-06-08T19:00:00",
            ).exists()
        )

    def test_retrieve_performance(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-06-08T19:00:00",
        )
        url = reverse("theatre:performance-detail", kwargs={"pk": performance.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], performance.id)
        self.assertEqual(response.data["play"]["id"], self.play.id)
        self.assertEqual(response.data["theatre_hall"]["id"], self.theatre_hall.id)
        self.assertEqual(response.data["show_time"], "2024-06-08T19:00:00")

    def test_update_performance(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-06-08T19:00:00",
        )
        url = reverse("theatre:performance-detail", kwargs={"pk": performance.id})
        updated_data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2024-06-01T20:00:00",
        }
        self.client.force_authenticate(user=self.admin)

        response = self.client.put(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        performance.refresh_from_db()

        self.assertEqual(performance.play.id, self.play.id)
        self.assertEqual(performance.theatre_hall.id, self.theatre_hall.id)

        self.assertEqual(str(performance.show_time), "2024-06-01 20:00:00")
