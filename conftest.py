# conftest.py

import pytest
import requests
from utils import BASE_URL, generate_random_string

@pytest.fixture
def new_courier():
    """Фикстура для создания нового курьера перед тестом и удаления после теста."""
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)
    assert response.status_code == 201, "Не удалось создать курьера в фикстуре"

    # Получаем ID курьера
    login_payload = {
        "login": login,
        "password": password
    }
    login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=login_payload)
    assert login_response.status_code == 200, "Не удалось авторизоваться в фикстуре"
    courier_id = login_response.json()["id"]

    courier_data = {
        "id": courier_id,
        "login": login,
        "password": password
    }

    yield courier_data  # Возвращаем данные курьера в тест

    # Удаляем курьера после теста
    requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')