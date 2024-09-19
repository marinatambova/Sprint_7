import pytest
from utils import create_courier, login_courier, delete_courier

@pytest.fixture
def new_courier():
    """Фикстура для создания курьера перед тестом и удаления после теста."""
    # Создаём курьера
    create_response, courier_payload = create_courier()
    assert create_response.status_code == 201, "Не удалось создать курьера в фикстуре"

    # Получаем данные курьера
    login = courier_payload["login"]
    password = courier_payload["password"]
    first_name = courier_payload["firstName"]

    # Авторизуемся, чтобы получить ID курьера
    login_response = login_courier(login, password)
    assert login_response.status_code == 200, "Не удалось авторизоваться в фикстуре"
    courier_id = login_response.json()["id"]

    courier_data = {
        "id": courier_id,
        "login": login,
        "password": password,
        "first_name": first_name
    }

    yield courier_data  # Передаем данные курьера в тест

    # Удаляем курьера после теста
    delete_response = delete_courier(courier_id)
    assert delete_response.status_code == 200, "Не удалось удалить курьера в фикстуре"