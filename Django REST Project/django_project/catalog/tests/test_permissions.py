import random
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase
from accounting.models import User
from catalog.models import Category, Product, Tag


class PermissionsTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test", email="test@mail.com", password="password")
        cls.admin_user = User.objects.create_user(
            username="superuser",
            email="superuser@mail.com",
            password="password",
            is_staff=True,
            is_superuser=False,
        )

        cls.category_count = 3
        cls.tags_count = 10
        cls.products_count = 10

        categories = [
            Category.objects.create(name=f"Категория {i}", description=f"Описание {i}")
            for i in range(cls.category_count)
        ]
        tags = [Tag.objects.create(name=f"Тег {i}") for i in range(cls.tags_count)]
        for i in range(cls.products_count):
            product = Product.objects.create(
                name=f"Ноутбук v{i}",
                description="Описание товара",
                price=Decimal("1000.0"),
                stock=10,
                category=random.choice(categories),
            )
            product.tags.set([random.choice(tags), random.choice(tags)])

        cls.category_list_create_url = reverse("category-list")
        cls.category_detail_url = reverse("category-detail", kwargs={"pk": categories[0].id})

    def test_category_list_api_view_anon(self):
        self._check_category_list()

    def test_category_list_api_view_user(self):
        self.client.force_login(self.user)
        self._check_category_list()

    def test_category_list_api_view_admin_user(self):
        self.client.force_login(self.admin_user)
        self._check_category_list()

    def _check_category_list(self):
        resp = self.client.get(self.category_list_create_url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("count", resp.data)
        self.assertEqual(resp.data["count"], self.category_count)
        self.assertIn("results", resp.data)
        self.assertEqual(len(resp.data["results"]), self.category_count)
        self.assertIn("next", resp.data)
        self.assertIn("previous", resp.data)

    def test_category_create_api_view_anon(self):
        resp = self.client.post(
            self.category_list_create_url,
            data={
                "name": "Компьютерная техника",
                "description": "Описание категории",
            },
        )
        self.assertEqual(resp.status_code, 401)

    def test_category_create_api_view_user(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            self.category_list_create_url,
            data={
                "name": "Компьютерная техника",
                "description": "Описание категории",
            },
        )
        self.assertEqual(resp.status_code, 403)

    def test_category_create_api_view_admin_user(self):
        self.client.force_login(self.admin_user)
        resp = self.client.post(
            self.category_list_create_url,
            data={
                "name": "Компьютерная техника",
                "description": "Описание категории",
            },
        )
        self.assertEqual(resp.status_code, 201)

        self.assertEqual(Category.objects.count(), self.category_count + 1)
