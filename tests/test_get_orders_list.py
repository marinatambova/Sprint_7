# test_get_orders_list.py

import pytest
import requests
from config import BASE_URL, GET_ORDERS_ENDPOINT

@pytest.mark.get_orders_list
class TestGetOrdersList:

    def test_get_orders_list_returns_orders(self):
        url = BASE_URL + GET_ORDERS_ENDPOINT

        response = requests.get(url)

        assert response.status_code == 200, "Некорректный код ответа при получении списка заказов"
        assert "orders" in response.json(), "В ответе отсутствует ключ 'orders'"
        assert isinstance(response.json()["orders"], list), "'orders' должен быть списком"
        assert len(response.json()["orders"]) > 0, "Список заказов пуст"