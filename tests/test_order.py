import requests
import allure
import pytest
from faker import Faker

from urls import Urls

fake = Faker()


class TestOrderCreate:
    data = [
        {"firstName": "Guido",
         "lastName": "van Rossum",
         "address": "Pushkinova, 34",
         "metroStation": 9,
         "phone": "+79999999999",
         "rentTime": 2,
         "deliveryDate": "2024-07-07",
         "comment": "just test comment 1",
         "color": []},
        {"firstName": "Mister",
         "lastName": "Blackgrey",
         "address": "Tolstoeva 12",
         "metroStation": 10,
         "phone": "89999999999",
         "rentTime": 3,
         "deliveryDate": "2024-08-08",
         "comment": "just test comment 2",
         "color": ["BLACK", "GREY"]},
        {"firstName": "Mister",
         "lastName": "Black",
         "address": "ул. Главная 13-13",
         "metroStation": 11,
         "phone": "+7 999 999 99 99",
         "rentTime": 4,
         "deliveryDate": "2024-09-09",
         "comment": "just test comment 3",
         "color": ["BLACK"]},
        {"firstName": "Mister",
         "lastName": "Grey",
         "address": "улица Комсомольскнаамурова д.5 кв. 55",
         "metroStation": 12,
         "phone": "8-999-999-99-99",
         "rentTime": 5,
         "deliveryDate": "2024-10-10",
         "comment": "just test comment 4",
         "color": ["GREY"]}
    ]

    @allure.title('Проверка успешного создания заказа')
    @allure.description('При создании заказа передаются все обязательные и необязательные поля. Среди необязательных полей передаются данные о цвете скутера для заказа, ввключая один из двух возможных цветов, либо оба.')
    @pytest.mark.parametrize("order_data", data)
    # тут два теста с отправкой одного цвета будут падать, так как, видимо, в API баг
    def test_order_create_required_fields_success_create(self, order_data):
        response = requests.post(Urls.ORDER_MAIN_URL, data=order_data)
        assert response.status_code == 201 and 'track' in response.json()


class TestGetOrdersList:
    @allure.title('Проверка успешного получения списка заказов')
    @allure.description('При получении списка заказа не передаются параметры')
    def test_get_order_list(self):
        response = requests.get(Urls.ORDER_MAIN_URL)
        assert type(response.json()['orders']) == list and 'id' in response.json()['orders'][0]


class TestGetOrder:
    @allure.title('Проверка получения несуществующего заказа')
    @allure.description('При получении заказа передаются несуществующий номер')
    def test_get_order_nonexistent_track_error_message(self):
        payload = {'t': '255499999'}
        response = requests.get(Urls.ORDER_TRACK_URL, params=payload)
        assert response.status_code == 404 and response.json()['message'] == 'Заказ не найден'

    @allure.title('Проверка получения заказа без номера')
    @allure.description('При получении заказа не передается номер')
    def test_get_order_no_track_error_message(self):
        response = requests.get(Urls.ORDER_TRACK_URL)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для поиска'

    @allure.title('Проверка получения существующего заказа')
    @allure.description('При получении заказа передаются номер существующего заказа')
    def test_get_order_existent_track_success_message(self, created_order):
        payload = {'t': created_order}
        response = requests.get(Urls.ORDER_TRACK_URL, params=payload)
        assert response.status_code == 200 and 'id' in response.json()['order']
