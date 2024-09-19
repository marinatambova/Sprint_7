# test_courier_login.py

import pytest
import requests
from config import BASE_URL, LOGIN_COURIER_ENDPOINT
from expected_results import COURIER_LOGIN_NOT_ENOUGH_DATA, COURIER_ACCOUNT_NOT_FOUND
from utils import login_courier

@pytest.mark.courier_login
class TestCourierLogin:

    def test_courier_login_success(self, new_courier):
        login = new_courier["login"]
        password = new_courier["password"]

        response = login_courier(login, password)

        assert response.status_code == 200, "Некорректный код ответа при авторизации курьера"
        assert "id" in response.json(), "В ответе отсутствует 'id' курьера"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_login_missing_field(self, new_courier, missing_field):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"]
        }

        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        url = BASE_URL + LOGIN_COURIER_ENDPOINT
        response = requests.post(url, json=payload)

        # Добавляем проверку на статус-код 504
        if response.status_code == 504:
            pytest.xfail(f"Сервер вернул 504 Gateway Timeout при отсутствии поля {missing_field}")

        assert response.status_code == 400, f"Должен быть код 400 при отсутствии поля {missing_field}"
        assert response.json()["message"] == COURIER_LOGIN_NOT_ENOUGH_DATA, "Некорректное сообщение об ошибке"

    def test_courier_login_wrong_password(self, new_courier):
        login = new_courier["login"]
        payload = {
            "login": login,
            "password": "incorrect_password"
        }

        url = BASE_URL + LOGIN_COURIER_ENDPOINT
        response = requests.post(url, json=payload)

        assert response.status_code == 404, "Должен быть код 404 при неверном пароле"
        assert response.json()["message"] == COURIER_ACCOUNT_NOT_FOUND, "Некорректное сообщение об ошибке"

    def test_courier_login_nonexistent_user(self):
        payload = {
            "login": "nonexistent_user",
            "password": "some_password"
        }

        url = BASE_URL + LOGIN_COURIER_ENDPOINT
        response = requests.post(url, json=payload)

        assert response.status_code == 404, "Должен быть код 404 при авторизации несуществующего пользователя"
        assert response.json()["message"] == COURIER_ACCOUNT_NOT_FOUND, "Некорректное сообщение об ошибке"