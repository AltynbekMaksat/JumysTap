from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import JobSeekerProfile, User


class UsersAPITests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass2026!",
            role="job_seeker",
        )

    def test_registration(self) -> None:
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "StrongPass2026!",
                "password_confirmation": "StrongPass2026!",
                "role": "job_seeker",
            },
        )

        print("Registration:", response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_login(self) -> None:
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "StrongPass2026!",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_requires_authentication(self) -> None:
        response = self.client.get(reverse("users:user_me"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("users:user_me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_update_me(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse("users:user_me"),
            {"first_name": "Maksat"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Maksat")

    def test_create_profile(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse("users:job_seeker_profile"),
            {
                "phone": "+77001234567",
                "city": "Almaty",
                "bio": "Junior Django Developer",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            JobSeekerProfile.objects.filter(user=self.user).exists()
        )

    def test_employer_cannot_create_profile(self) -> None:
        employer = User.objects.create_user(
            username="employer",
            email="employer@example.com",
            password="StrongPass2026!",
            role="employer",
        )

        self.client.force_authenticate(user=employer)

        response = self.client.post(
            reverse("users:job_seeker_profile"),
            {"city": "Almaty"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )