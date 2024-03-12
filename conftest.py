import pytest
import requests
from faker import Faker

fake = Faker()


@pytest.fixture
def created_courier():
    login = 'iamtestcourier' + str(fake.random_int(0, 9999))
    password = 'password' + str(fake.random_int(0, 9999))
    first_name = 'Courier' + str(fake.random_int(0, 9999))
    payload = {'login': login, 'password': password, 'firstName': first_name}
    requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/', data=payload)
    login_payload = {'login': login, 'password': password}
    login_response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=login_payload)
    courier_id = login_response.json().get('id')
    return courier_id


@pytest.fixture
def created_order():
    data = {"firstName": "Mister",
            "lastName": "Blackgrey",
            "address": "Tolstoeva 12",
            "metroStation": 10,
            "phone": "89999999999",
            "rentTime": 3,
            "deliveryDate": "2024-08-08",
            "comment": "just test comment 2",
            "color": ["BLACK", "GREY"]}

    response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/orders/', data=data)
    track = response.json().get('track')
    return track
