from lib.base_case import BaseCase
import requests
from lib.assertions import Assertions


class TestListUsersGet(BaseCase):
    LIST_USERS_URL = 'api/users'

    def test_list_users_post_response_code(self):
        data = self.prepare_post_data()
        list_users_response = requests.post(f'{self.BASE_URL}{self.LIST_USERS_URL}', data=data)
        Assertions.assert_code_status(list_users_response, 201)

    def test_list_users_post_response_code_negative(self):
        data = self.prepare_post_data()
        list_users_response = requests.post(f'{self.BASE_URL}{self.LIST_USERS_URL}', data=data)
        Assertions.assert_code_status(list_users_response, 201)

    def test_list_users_post_response_has_fields(self):
        data = self.prepare_post_data()
        list_users_response = requests.post(f'{self.BASE_URL}{self.LIST_USERS_URL}', data=data)
        expected_fields = ['name', 'job', 'id', 'createdAt']
        Assertions.assert_json_value_has_keys(list_users_response, expected_fields)

    def test_list_users_post_response_data(self):
        data = self.prepare_post_data()
        list_users_response = requests.post(f'{self.BASE_URL}{self.LIST_USERS_URL}', data=data)
        for key, expected_value in data.items():
            real_value = self.get_json_value(list_users_response, key)
            assert expected_value == real_value, f'expected {key} is {expected_value}, ' \
                                                                          f'but {key} is {real_value}'

    def test_list_users_post_response_data_type(self):
        data = self.prepare_post_data()
        list_users_response = requests.post(f'{self.BASE_URL}{self.LIST_USERS_URL}', data=data)
        for key, expected_value in data.items():
            real_value = self.get_json_value(list_users_response, key)
            assert type(expected_value) == type(real_value), f'expected {key} type is {expected_value}, ' \
                                                                          f'but {key} type is {real_value}'