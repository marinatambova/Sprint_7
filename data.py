from generate_random_string import generate_random_string

def get_courier_payload(login=None, password=None, first_name=None):
    """Возвращает payload для создания курьера."""
    if login is None:
        login = generate_random_string()
    if password is None:
        password = generate_random_string()
    if first_name is None:
        first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return payload

def get_order_payload(color=None):
    """Возвращает payload для создания заказа."""
    if color is None:
        color = []
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": color
    }
    return payload