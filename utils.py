import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

def generate_random_string(length=10):
    """Генерирует случайную строку из букв нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_courier():
    """Создаёт нового курьера и возвращает его данные."""
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/api/v1/courier', json=payload)
    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "firstName": first_name
        }
    else:
        print(f"Не удалось создать курьера: {response.status_code}, {response.text}")
        return None

def delete_courier(courier_id):
    """Удаляет курьера по его ID."""
    response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    if response.status_code == 200:
        return True
    else:
        print(f"Не удалось удалить курьера: {response.status_code}, {response.text}")
        return False