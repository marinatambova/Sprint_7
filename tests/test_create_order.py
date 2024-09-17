import requests
import pytest
from utils import BASE_URL

@pytest.mark.create_order
class TestCreateOrder:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, color):
        """Проверка создания заказа с разными вариантами цвета."""
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }

        response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)

        assert response.status_code == 201, "Некорректный код ответа при создании заказа"
        assert "track" in response.json(), "В ответе отсутствует 'track' номера заказа"

    def test_create_order_response_contains_track(self):
        """Тело ответа содержит track."""
        payload = {
            "firstName": "Sakura",
            "lastName": "Haruno",
            "address": "Konoha, 143 apt.",
            "metroStation": 5,
            "phone": "+7 800 355 35 36",
            "rentTime": 3,
            "deliveryDate": "2020-06-07",
            "comment": "Naruto, вернись!",
            "color": []
        }

        response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)

        assert response.status_code == 201, "Некорректный код ответа при создании заказа"
        assert "track" in response.json(), "В ответе отсутствует 'track' номера заказа"