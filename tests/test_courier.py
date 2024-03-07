import requests
import allure
import pytest
from data import Data
from faker import Faker

fake = Faker()


class TestCourierLogin:

    @allure.title('Проверка залогинивания существующего курьера')
    @allure.description('При залогинивании курьера, используются существующий логин и пароль')
    def test_courier_login_existent_user_success_login(self):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=Data.actual_courier_credentials)
        assert response.status_code == 200 and 'id' in response.json()

    @allure.title('Проверка залогинивания несуществующего курьера')
    @allure.description('При залогинивании курьера, используются несуществующий логин и пароль')
    def test_courier_login_nonexistent_user_error_response(self):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=Data.nonexistent_courier_credentials)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка залогинивания курьера с неправильным паролем')
    @allure.description('При залогинивании курьера, используются существующий логин и неправильный пароль')
    def test_courier_login_wrong_password_error_response(self):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=Data.actual_courier_wrong_password)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка залогинивания при отправке пустых полей')
    @allure.description('При залогинивании курьера, передаются пустые поля для логина, пароля и для обеих полей')
    @pytest.mark.parametrize("missing_credentials", [
        {'login': '', 'password': ''},
        {'login': 'ninjaty', 'password': ''},
        {'login': '', 'password': '4434343'}
    ])
    def test_courier_login_missing_credentials_error_response(self, missing_credentials):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=missing_credentials)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'

    @allure.title('Проверка залогинивания при отправке не всех полей')
    @allure.description('При залогинивании курьера, передаются не все поля')
    @pytest.mark.parametrize("missing_fields", [{'password': '12345'}, {'login': 'ninjaty'}, {}])
    # тут успешной будет только проверка при отсутствии поля "login", так как для двух остальных случаев кажется в API есть баги
    def test_courier_login_missing_fields_error_response(self, missing_fields):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=missing_fields)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'


class TestCourierCreate:

    @allure.title('Проверка успешного создания курьера')
    @allure.description('При создании курьера передаются все три поля: login, password, firstName')
    def test_courier_create_success_create(self):
        login = 'iamtestcourier' + str(fake.random_int(0, 9999))
        password = 'password' + str(fake.random_int(0, 9999))
        first_name = 'Courier' + str(fake.random_int(0, 9999))
        payload = {'login': login, 'password': password, 'firstName': first_name}
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/', data=payload)
        assert response.status_code == 201 and response.json() == {'ok': True}
        # удалим созданного курьера
        login_payload = {'login': login, 'password': password}
        login_response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                       data=login_payload)
        courier_id = login_response.json().get('id')
        delete_response = requests.delete(f'http://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}/')
        assert delete_response.status_code == 200 and delete_response.json() == {'ok': True}

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    @allure.description('При создании курьера, используются все креды уже созданного курьера')
    def test_courier_login_existent_user_error_message(self):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/',
                                 data=Data.created_courier_credentials)
        assert response.status_code == 409 and response.json()[
            'message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка невозможности создания курьера с логином, который уже есть')
    @allure.description('При создании курьера, используется логин существующего курьера, пароль и имя - генерируются')
    def test_courier_login_existent_user_login_error_message(self):
        password = 'password' + str(fake.random_int(0, 9999))
        first_name = 'Courier' + str(fake.random_int(0, 9999))
        payload = {'login': 'heyitsme', 'password': password, 'firstName': first_name}
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/', data=payload)
        assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка невозможности создания курьера если передаются пустые поля')
    @allure.description('При создании курьера одно, два или три поля остаются пустыми')
    @pytest.mark.parametrize("missing_credentials", [
        {'login': '', 'password': '', 'firstName': ''},
        {'login': "iamtestcourier" + str(fake.random_int(0, 9999)), 'password': '', 'firstName': ''},
        {'login': "iamtestcourier" + str(fake.random_int(0, 9999)), 'password': '4434343', 'firstName': ''},
        {'login': "iamtestcourier" + str(fake.random_int(0, 9999)), 'password': '', 'firstName': 'Iamtestcourier'},
        {'login': '', 'password': '', 'firstName': 'Iamtestcourier'},
        {'login': '', 'password': '4434343', 'firstName': ''},
        {'login': '', 'password': '4434343', 'firstName': 'Iamtestcourier'}
    ])
    # тут один тест будет падать, так как, по всей видимости поле 'firstName' не является обязательным
    def test_courier_login_empty_fields_error_message(self, missing_credentials):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/', data=missing_credentials)
        assert response.status_code == 400

    @allure.title('Проверка невозможности создания курьера если не передаются поля')
    @allure.description('При создании курьера одно, два или три поля не передается')
    @pytest.mark.parametrize("missing_credentials", [
        {},
        {'login': "iamtestcourier" + str(fake.random_int(0, 9999)), 'password': '4434343'},
        {'login': "iamtestcourier" + str(fake.random_int(0, 9999)), 'firstName': 'Iamtestcourier'},
        {'login': "iamtestcourier" + str(fake.random_int(0, 9999))},
        {'password': '4434343', 'firstName': 'Iamtestcourier'},
        {'password': '4434343'},
        {'firstName': 'Iamtestcourier'}
    ])
    # тут один тест будет падать, так как, по всей видимости поле 'firstName' не является обязательным
    def test_courier_login_no_fields_error_message(self, missing_credentials):
        response = requests.post('http://qa-scooter.praktikum-services.ru/api/v1/courier/', data=missing_credentials)
        assert response.status_code == 400


class TestCourierDelete:
    @allure.title('Проверка невозможности удаления несуществующего курьера')
    @allure.description('При удалении курьера, используется несуществующий "id"')
    def test_courier_delete_nonexistent_id_error_message(self):
        response = requests.delete('http://qa-scooter.praktikum-services.ru/api/v1/courier/270999999')
        assert response.status_code == 404 and response.json()['message'] == 'Курьера с таким id нет.'

    @allure.title('Проверка невозможности удаления курьера при неполном запросе')
    @allure.description('При удалении курьера не передается "id"')
    # тут тест будет падать так как кажется в API есть баги
    def test_courier_delete_no_id_error_message(self):
        response = requests.delete('http://qa-scooter.praktikum-services.ru/api/v1/courier/')
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для удаления курьера'

    @allure.title('Проверка успешного удаления курьера')
    @allure.description('При удалении передается "id" созданного в фикстуре курьера')
    def test_courier_delete_existent_id_success_message(self, created_courier):
        response = requests.delete(f'http://qa-scooter.praktikum-services.ru/api/v1/courier/{created_courier}')
        assert response.status_code == 200 and response.json() == {'ok': True}


