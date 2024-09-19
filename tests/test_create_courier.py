import pytest
import requests
from config import BASE_URL, CREATE_COURIER_ENDPOINT
from data import get_courier_payload
from utils import login_courier, delete_courier
from expected_results import COURIER_LOGIN_ALREADY_USED, COURIER_NOT_ENOUGH_DATA
from generate_random_string import generate_random_string

@pytest.mark.create_courier
class TestCreateCourier:

    def test_create_courier_success(self):
        payload = get_courier_payload()

        url = BASE_URL + CREATE_COURIER_ENDPOINT
        response = requests.post(url, json=payload)

        assert response.status_code == 201, "Некорректный код ответа при создании курьера"
        assert response.json()["ok"] == True, "В теле ответа отсутствует 'ok': true"

        # Удаляем созданного курьера
        login = payload["login"]
        password = payload["password"]
        login_response = login_courier(login, password)
        courier_id = login_response.json()["id"]
        delete_response = delete_courier(courier_id)
        assert delete_response.status_code == 200, "Не удалось удалить курьера после теста"

    def test_create_same_courier_fail(self, new_courier):
        payload = get_courier_payload(
            login=new_courier["login"],
            password=new_courier["password"],
            first_name=generate_random_string()
        )

        url = BASE_URL + CREATE_COURIER_ENDPOINT
        response = requests.post(url, json=payload)

        assert response.status_code == 409, "Должен быть код 409 при создании курьера с существующим логином"
        assert response.json()["message"] == COURIER_LOGIN_ALREADY_USED, "Некорректное сообщение об ошибке"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_with_missing_field(self, missing_field):
        payload = get_courier_payload()

        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        url = BASE_URL + CREATE_COURIER_ENDPOINT
        response = requests.post(url, json=payload)

        assert response.status_code == 400, f"Должен быть код 400 при отсутствии поля {missing_field}"
        assert response.json()["message"] == COURIER_NOT_ENOUGH_DATA, "Некорректное сообщение об ошибке"