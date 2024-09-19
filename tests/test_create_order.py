# test_create_order.py

import pytest
import requests
from config import BASE_URL, CREATE_ORDER_ENDPOINT
from data import get_order_payload

@pytest.mark.create_order
class TestCreateOrder:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, color):
        payload = get_order_payload(color=color)

        url = BASE_URL + CREATE_ORDER_ENDPOINT
        response = requests.post(url, json=payload)

        assert response.status_code == 201, "Некорректный код ответа при создании заказа"
        assert "track" in response.json(), "В ответе отсутствует 'track' номера заказа"