# test_create_courier.py

import requests
import pytest
from utils import BASE_URL, generate_random_string

@pytest.mark.create_courier
class TestCreateCourier:

    def test_create_courier_success(self):
        """Курьера можно создать с корректными данными."""
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)

        assert response.status_code == 201, "Некорректный код ответа при создании курьера"
        assert response.json()["ok"] == True, "В теле ответа отсутствует 'ok': true"

        # Удаление созданного курьера после теста
        # Авторизуемся, чтобы получить ID курьера
        login_payload = {
            "login": login,
            "password": password
        }
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=login_payload)
        courier_id = login_response.json()["id"]

        # Удаляем курьера
        requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')

    def test_create_same_courier_fail(self, new_courier):
        """Нельзя создать двух одинаковых курьеров."""
        # Используем данные курьера из фикстуры
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": generate_random_string()
        }

        # Пытаемся создать курьера с тем же логином
        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)
        assert response.status_code == 409, "Должен быть код 409 при создании курьера с существующим логином"
        # Обновленная проверка сообщения об ошибке
        assert "Этот логин уже используется" in response.json()["message"], "Некорректное сообщение об ошибке"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_with_missing_field(self, missing_field):
        """Проверка создания курьера без одного из обязательных полей."""
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }

        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)

        assert response.status_code == 400, f"Должен быть код 400 при отсутствии поля {missing_field}"
        assert "Недостаточно данных для создания учетной записи" in response.json()["message"], "Некорректное сообщение об ошибке"

    def test_create_courier_without_first_name(self):
        """Проверка создания курьера без поля firstName (опционально)."""
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string()
            # Поле 'firstName' отсутствует
        }

        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)

        # Проверяем, что курьер успешно создаётся без firstName
        assert response.status_code == 201, "Ожидался код 201 при создании курьера без firstName"
        assert response.json()["ok"] == True, "В теле ответа отсутствует 'ok': true"

        # Удаление созданного курьера
        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=login_payload)
        courier_id = login_response.json()["id"]
        requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')

    def test_create_courier_with_existing_login(self, new_courier):
        """Попытка создания курьера с логином, который уже есть."""
        # Пробуем создать другого курьера с тем же логином
        payload = {
            "login": new_courier["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }

        response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)
        assert response.status_code == 409, "Должен быть код 409 при создании курьера с существующим логином"
        # Обновленная проверка сообщения об ошибке
        assert "Этот логин уже используется" in response.json()["message"], "Некорректное сообщение об ошибке"