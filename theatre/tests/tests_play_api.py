import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Performance, TheatreHall, Genre, Actor
from theatre.serializers import PlayListSerializer, PlayDetailSerializer

PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Crazy Day or the Marriage of Figaro",
        "description": "Based on the novel by Beaumarchais",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Vaudeville",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "Jude", "last_name": "Law"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Piccolo Teatro di Milano", rows=30, seats_in_row=45
    )

    defaults = {
        "show_time": "2024-06-08 19:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def image_upload_url(play_id):
    """
    Return URL for recipe image upload
    """

    return reverse("theatre:play-upload-image", args=[play_id])


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testPassword"
        )
        self.client.force_authenticate(self.user)
        self.play = sample_play()
        self.genre = sample_genre()
        self.actor = sample_actor()

    def test_plays_list(self):
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)

        res = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_filter_plays_by_title(self):
        play_with_title = sample_play(title="Title")

        res = self.client.get(PLAY_URL, {"title": "Title"})

        serializer_without_title = PlayListSerializer(self.play)
        serializer_with_title = PlayListSerializer(play_with_title)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_title.data, res.data.get("results"))
        self.assertNotIn(serializer_without_title.data, res.data.get("results"))

    def test_filter_plays_by_genre(self):
        play_without_genre = sample_play()
        self.play.genres.add(self.genre)

        res = self.client.get(PLAY_URL, {"genres": self.genre.id})

        serializer_without_genre = PlayListSerializer(play_without_genre)
        serializer_with_genre = PlayListSerializer(self.play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_genre.data, res.data.get("results"))
        self.assertNotIn(serializer_without_genre.data, res.data.get("results"))

    def test_filter_plays_by_actor(self):
        play_without_actor = sample_play()
        self.play.actors.add(self.actor)

        res = self.client.get(PLAY_URL, {"actors": self.actor.id})

        serializer_with_actor = PlayListSerializer(self.play)
        serializer_without_actor = PlayListSerializer(play_without_actor)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_actor.data, res.data.get("results"))
        self.assertNotIn(serializer_without_actor.data, res.data.get("results"))

    def test_play_detail(self):
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)

        res = self.client.get(detail_url(self.play.id))

        serializer = PlayDetailSerializer(self.play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Forbidden play",
            "description": "Forbidden description",
        }
        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="adminPassword",
        )
        self.client.force_authenticate(self.user)
        self.play = sample_play()
        self.genre = sample_genre()
        self.actor = sample_actor()
        self.performance = sample_performance(play=self.play)

    def test_create_play_successful(self):
        payload = {
            "title": "Successful play",
            "description": "Successful description",
        }
        res = self.client.post(PLAY_URL, payload)

        play = Play.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(play, key))

    def test_create_play_with_genres(self):
        genre_1 = self.genre
        genre_2 = sample_genre(name="Name")
        payload = {
            "title": "Successful play",
            "description": "Successful description",
            "genres": (genre_1.id, genre_2.id,),
        }

        res = self.client.post(PLAY_URL, payload)

        play = Play.objects.get(id=res.data["id"])
        genre = play.genres.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(genre_1, genre)
        self.assertIn(genre_2, genre)
        self.assertEqual(genre.count(), 2)

    def test_create_play_with_actors(self):
        actor_1 = self.actor
        actor_2 = sample_actor(first_name="Firstname", last_name="Lastname")
        payload = {
            "title": "Successful play",
            "description": "Successful description",
            "actors": (actor_1.id, actor_2.id,),
        }

        res = self.client.post(PLAY_URL, payload)

        play = Play.objects.get(id=res.data["id"])
        actor = play.actors.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(actor_1, actor)
        self.assertIn(actor_2, actor)
        self.assertEqual(actor.count(), 2)

    def test_update_play_not_allowed(self):
        url = detail_url(self.play.id)

        res = self.client.post(url, {"title": "Title"})
        # print(res.data)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_play_not_allowed(self):
        url = detail_url(self.play.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def tearDown(self):
        self.play.image.delete()

    def test_upload_image_to_play(self):
        """
        Test uploading an image to play
        """

        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.play.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.play.image.path))

    def test_upload_image_bad_request(self):
        """
        Test uploading an invalid image
        """

        url = image_upload_url(self.play.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_play_list_should_not_work(self):
        url = PLAY_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "title": "Title",
                    "description": "Description",
                    "genres": [1],
                    "actors": [1],
                    "image": ntf,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        play = Play.objects.get(title="Title")
        self.assertFalse(play.image)

    def test_image_url_is_shown_on_play_detail(self):
        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(detail_url(self.play.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_play_list(self):
        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(PLAY_URL)

        self.assertIn("image", res.data.get("results")[0].keys())

    def test_image_url_is_shown_on_performance_detail(self):
        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(PERFORMANCE_URL)

        self.assertIn("play_image", res.data.get("results")[0].keys())
