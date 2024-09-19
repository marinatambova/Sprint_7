# utils.py

import requests
from config import (BASE_URL, CREATE_COURIER_ENDPOINT, LOGIN_COURIER_ENDPOINT,
                    DELETE_COURIER_ENDPOINT, CREATE_ORDER_ENDPOINT)
from generate_random_string import generate_random_string

def create_courier(login=None, password=None, first_name=None):
    """Создаёт курьера с указанными данными или случайно сгенерированными."""
    if login is None:
        login = generate_random_string()
    if password is None:
        password = generate_random_string()
    if first_name is None:
        first_name = generate_random_string()

    url = BASE_URL + CREATE_COURIER_ENDPOINT
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(url, json=payload)
    return response, payload  # Возвращаем ответ и payload для дальнейшего использования

def login_courier(login, password):
    """Авторизует курьера и возвращает ответ сервера."""
    url = BASE_URL + LOGIN_COURIER_ENDPOINT
    payload = {
        "login": login,
        "password": password
    }

    response = requests.post(url, json=payload)
    return response

def delete_courier(courier_id):
    """Удаляет курьера по его ID."""
    url = BASE_URL + DELETE_COURIER_ENDPOINT.format(courier_id=courier_id)
    response = requests.delete(url)
    return response

def create_order(order_data):
    """Создаёт заказ с указанными данными."""
    url = BASE_URL + CREATE_ORDER_ENDPOINT
    response = requests.post(url, json=order_data)
    return response