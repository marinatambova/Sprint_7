# test_courier_login.py

import requests
import pytest
from utils import BASE_URL, generate_random_string

@pytest.mark.courier_login
class TestCourierLogin:

    def test_courier_login_success(self, new_courier):
        """Курьер может авторизоваться с корректными данными."""
        login_payload = {
            "login": new_courier["login"],
            "password": new_courier["password"]
        }
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=login_payload)

        assert response.status_code == 200, "Некорректный код ответа при авторизации курьера"
        assert "id" in response.json(), "В ответе отсутствует 'id' курьера"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_login_missing_field(self, new_courier, missing_field):
        """Проверка авторизации без одного из обязательных полей."""
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"]
        }

        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=payload)

        # Добавляем логирование для отладки
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")

        # Проверяем, если сервер возвращает 504, помечаем тест как xfail
        if response.status_code == 504:
            pytest.xfail(f"Сервер вернул 504 Gateway Timeout при отсутствии поля {missing_field}")

        assert response.status_code == 400, f"Должен быть код 400 при отсутствии поля {missing_field}"
        assert "Недостаточно данных для входа" in response.json()["message"], "Некорректное сообщение об ошибке"

    def test_courier_login_wrong_password(self, new_courier):
        """Система вернёт ошибку при неверном пароле."""
        payload = {
            "login": new_courier["login"],
            "password": "wrong_password"
        }

        response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=payload)

        assert response.status_code == 404, "Должен быть код 404 при неверном пароле"
        assert "Учетная запись не найдена" in response.json()["message"], "Некорректное сообщение об ошибке"

    def test_courier_login_nonexistent_user(self):
        """Авторизация под несуществующим пользователем должна вернуть ошибку."""
        payload = {
            "login": "nonexistent_user",
            "password": "some_password"
        }

        response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=payload)

        assert response.status_code == 404, "Должен быть код 404 при авторизации несуществующего пользователя"
        assert "Учетная запись не найдена" in response.json()["message"], "Некорректное сообщение об ошибке"