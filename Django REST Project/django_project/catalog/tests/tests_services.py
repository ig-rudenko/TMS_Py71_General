from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from ..services import create_product, update_product
from ..models import Product, Category, Tag


class CreateProductTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product_price = Decimal("1000.0")
        cls.product_data: dict = {
            "name": "Ноутбук v1",
            "description": "Описание товара",
            "price": cls.product_price,
            "stock": 10,
            "category": {
                "name": "Компьютерная техника",
                "description": "Описание категории",
            },
            "tags": ["Ноутбук", "Игровой"],
        }

    def test_create_product_new(self):
        product = create_product(self.product_data)

        self.assertIsInstance(product, Product)
        self._assert_objects_count()
        self.assertEqual(product.price, self.product_price)

    def test_create_product_with_exists_category(self):
        Category.objects.create(**self.product_data["category"])

        create_product(self.product_data)

        self._assert_objects_count()

    def test_create_product_with_exists_tags(self):
        Tag.objects.create(name=self.product_data["tags"][0])

        create_product(self.product_data)

        self._assert_objects_count()

    def _assert_objects_count(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)

    def test_create_product_no_tags(self):
        self.product_data["tags"] = []
        create_product(self.product_data)

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 0)

    def test_create_product_check_rollback_with_tags_error(self):
        with patch("catalog.models.Tag.objects.get_or_create") as mock_get_or_create:
            mock_get_or_create.side_effect = ValueError()

            with self.assertRaises(ValueError):
                create_product(self.product_data)

        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)


class UpdateProductTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Компьютерная техника", description="Описание категории")
        self.product = Product.objects.create(
            name="Ноутбук v1",
            description="Описание товара",
            price=Decimal("1000.0"),
            stock=10,
            category=self.category,
        )

        self.tag1 = Tag.objects.create(name="Ноутбук")
        self.tag2 = Tag.objects.create(name="Игровой")

        self.product.tags.set([self.tag1, self.tag2])

    def test_update_product_simple(self):
        new_name = "Новое название"
        new_price = Decimal("2000.0")

        updated_product = update_product(
            self.product,
            {
                "name": new_name,
                "price": new_price,
            },
        )

        self.assertEqual(updated_product.name, new_name)
        self.assertEqual(updated_product.price, new_price)

        self.product.refresh_from_db()

        self.assertIs(updated_product, self.product)

        self.assertEqual(self.product.name, new_name)
        self.assertEqual(self.product.price, new_price)

    def test_update_product_category(self):
        new_category_data = {"name": "NEW", "description": "NEW DESC"}

        update_product(
            self.product,
            {"category": new_category_data},
        )

        self.product.category.refresh_from_db()

        self.assertEqual(self.product.category.name, new_category_data["name"])
        self.assertEqual(Category.objects.count(), 2)

    def test_update_product_with_exists_category(self):
        exists_category_data = {"name": self.category.name, "description": self.category.description}

        update_product(
            self.product,
            {"category": exists_category_data},
        )

        self.product.category.refresh_from_db()

        self.assertEqual(self.product.category.name, exists_category_data["name"])
        self.assertEqual(Category.objects.count(), 1)

    def test_update_product_tags(self):
        update_product(
            self.product,
            {"tags": ["new1", "new2"]},
        )

        self.assertEqual(self.product.tags.count(), 2)

        self.assertEqual(Tag.objects.count(), 4)

    def test_update_product_tags_2(self):
        update_product(
            self.product,
            {"tags": ["new1", "new2", self.tag1.name]},
        )

        self.assertEqual(self.product.tags.count(), 3)

        self.assertEqual(Tag.objects.count(), 4)

    def test_update_product_no_tags(self):
        update_product(
            self.product,
            {"tags": []},
        )

        self.assertEqual(self.product.tags.count(), 0)

        self.assertEqual(Tag.objects.count(), 2)
