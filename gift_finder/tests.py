from django.test import TestCase
from pydantic import ValidationError
from API.validators import RecommendedProduct


class RecommendedProductTests(TestCase):
    def test_valid_data(self):
        recommended_product = {
            "name": 'Ноутбук Apple MacBook Air 13" M1 8/256GB 2020',
            "price": "38 499₴",
            "image_url": "https://rozetka.com.ua/ua/apple_macbook_air_13_m1_256gb_2020_space_gray/p245161909/",
            "link": "https://rozetka.com.ua/ua/notebooks/c80004/",
        }

        try:
            RecommendedProduct(**recommended_product)
        except ValidationError as e:
            self.fail(f"Validation raised an unexpected exception: {e}")

    def test_invalid_name(self):
        recommended_product = {
            "name": {'Ноутбук Apple MacBook Air 13" M1 8/256GB 2020'},
            "price": "38 499₴",
            "image_url": "https://rozetka.com.ua/ua/apple_macbook_air_13_m1_256gb_2020_space_gray/p245161909/",
            "link": "https://rozetka.com.ua/ua/notebooks/c80004/",
        }

        with self.assertRaises(ValidationError):
            RecommendedProduct(**recommended_product)

    def test_invalid_price(self):
        recommended_product = {
            "name": 'Ноутбук Apple MacBook Air 13" M1 8/256GB 2020',
            "price": 38499,
            "image_url": "https://rozetka.com.ua/ua/apple_macbook_air_13_m1_256gb_2020_space_gray/p245161909/",
            "link": "https://rozetka.com.ua/ua/notebooks/c80004/",
        }

        with self.assertRaises(ValidationError):
            RecommendedProduct(**recommended_product)

    def test_invalid_product_img_url(self):
        recommended_product = {
            "name": 'Ноутбук Apple MacBook Air 13" M1 8/256GB 2020',
            "price": "38 499₴",
            "image_url": [
                "https://rozetka.com.ua/ua/apple_macbook_air_13_m1_256gb_2020_space_gray/p245161909/"
            ],
            "link": "https://rozetka.com.ua/ua/notebooks/c80004/",
        }

        with self.assertRaises(ValidationError):
            RecommendedProduct(**recommended_product)

    def test_invalid_product_url(self):
        recommended_product = {
            "name": 'Ноутбук Apple MacBook Air 13" M1 8/256GB 2020',
            "price": "38 499₴",
            "image_url": "https://rozetka.com.ua/ua/apple_macbook_air_13_m1_256gb_2020_space_gray/p245161909/",
            "link": {"https://rozetka.com.ua/ua/notebooks/c80004/"},
        }

        with self.assertRaises(ValidationError):
            RecommendedProduct(**recommended_product)
