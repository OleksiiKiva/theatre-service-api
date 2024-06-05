from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import Reservation, Play, Performance, TheatreHall

RESERVATION_URL = "/api/theatre/reservations/"


class ReservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testPassword"
        )
        content_type = ContentType.objects.get_for_model(Performance)
        permission, created = Permission.objects.get_or_create(
            codename="can_create_reservation",
            name="Can Create Reservation",
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(user=self.user)

        for _ in range(3):
            Reservation.objects.create(user=self.user)

        play = Play.objects.create(
            title="	Hamlet",
            description="Based on the novel by William Shakespeare"
        )
        theatre_hall = TheatreHall.objects.create(
            name="Piccolo Teatro di Milano", rows=40, seats_in_row=50
        )
        show_time = "2024-06-08T19:00:00"
        self.performance = Performance.objects.create(
            play_id=play.id,
            theatre_hall_id=theatre_hall.id,
            show_time=show_time,
        )

    def test_list_reservations(self):
        response = self.client.get(RESERVATION_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("count"), Reservation.objects.filter(user=self.user).count()
        )

    def test_create_reservation(self):
        data = {
            "tickets": [
                {"row": 10, "seat": 8, "performance": self.performance.id},
                {"row": 10, "seat": 9, "performance": self.performance.id},
            ]
        }
        response = self.client.post(RESERVATION_URL, data, format="json")

        created_reservation = Reservation.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("tickets", response.data)
        self.assertIn("created_at", response.data)
        self.assertEqual(created_reservation.user, self.user)
        self.assertEqual(created_reservation.tickets.count(), 2)
