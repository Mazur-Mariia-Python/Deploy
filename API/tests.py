from django.test import TestCase
import json
from rest_framework.test import APIClient
from pydantic import ValidationError
from .validators import QuestionnaireAnswers


from django.test import TestCase
from rest_framework.test import APIClient
from django.http import JsonResponse
from rest_framework import status
from pydantic import ValidationError
import json

class TestAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_load_response_data(self):
        input_data = {
            "budget": "1000",
            "male": "1",
            "age": "25",
            "date_type": "birthday",
            "hobbies": "Sport",
            "related_gifts": "original",
            "favorite_color": "green"
        }
        input_data_str = json.dumps({"_content": json.dumps(input_data)})  # Simulate the request structure

        response = self.client.post('/api/get_gifts/', data=input_data_str, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertIn('name', response_data[0])

    def test_api_load_response_data_validation_error(self):
        # Simulate invalid data to trigger validation error
        invalid_input_data_str = json.dumps({"_content": '{"invalid_key": "invalid_value"}'})

        response = self.client.post('/api/get_gifts/', data=invalid_input_data_str, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertIn('Validation error', response_data)


class QuestionnaireAnswersTests(TestCase):
    def test_valid_data(self):
        user_answers = {
            "budget": 55,
            "male": 2,
            "age": 58,
            "date_type": "Birthday",
            "hobbies": "sport",
            "related_gifts": "surprises and trinkets",
            "favorite_color": "black",
        }

        try:
            QuestionnaireAnswers(**user_answers)
        except ValidationError as e:
            self.fail(f"Validation raised an unexpected exception: {e}")

    def test_invalid_budget(self):
        user_answers = {
            "budget": -22,
            "male": 2,
            "age": 58,
            "date_type": "Birthday",
            "hobbies": "sport",
            "related_gifts": "surprises and trinkets",
            "favorite_color": "black",
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)

    def test_invalid_male(self):
        user_answers = {
            "budget": 450,
            "male": 3,
            "age": 66,
            "date_type": "Birthday",
            "hobbies": "music",
            "related_gifts": "surprises and trinkets",
            "favorite_color": "green",
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)

    def test_invalid_age(self):
        user_answers = {
            "budget": 120,
            "male": 1,
            "age": 0,
            "date_type": "Birthday",
            "hobbies": "sport",
            "related_gifts": "surprises and trinkets",
            "favorite_color": "blue",
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)

    def test_invalid_date_type(self):
        user_answers = {
            "budget": 120,
            "male": 2,
            "age": 47,
            "date_type": {1: "Birthday"},
            "hobbies": "sport",
            "related_gifts": "surprises and trinkets",
            "favorite_color": "blue",
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)

    def test_invalid_hobbies(self):
        user_answers = {
            "budget": 120,
            "male": 2,
            "age": 47,
            "date_type": "New Year",
            "hobbies": ["sport", "music"],
            "related_gifts": "surprises and trinkets",
            "favorite_color": "blue",
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)

    def test_invalid_related_gifts(self):
        user_answers = {
            "budget": 120,
            "male": 2,
            "age": 47,
            "date_type": "New Year",
            "hobbies": "music",
            "related_gifts": 6,
            "favorite_color": "violet",
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)

    def test_invalid_favorite_color(self):
        user_answers = {
            "budget": 120,
            "male": 2,
            "age": 47,
            "date_type": "New Year",
            "hobbies": "music",
            "related_gifts": 6,
            "favorite_color": ("violet", "black"),
        }

        with self.assertRaises(ValidationError):
            QuestionnaireAnswers(**user_answers)
