import requests
import pytest
from utils import BASE_URL

@pytest.mark.get_orders_list
class TestGetOrdersList:

    def test_get_orders_list_returns_orders(self):
        """Проверка, что в ответе возвращается список заказов."""
        response = requests.get(f'{BASE_URL}/api/v1/orders')

        assert response.status_code == 200, "Некорректный код ответа при получении списка заказов"
        assert "orders" in response.json(), "В ответе отсутствует ключ 'orders'"
        assert isinstance(response.json()["orders"], list), "'orders' должен быть списком"

        # Дополнительно можно проверить, что список не пустой, если ожидается наличие заказов
        assert len(response.json()["orders"]) > 0, "Список заказов пуст"