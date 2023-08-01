from lib.base_case import BaseCase
import requests
from lib.assertions import Assertions
import time
import re
import pytest

class TestListUsersGet(BaseCase):
    LIST_USERS_URL = 'api/users'
    delay_params = [
        (3),
        (4),
        (5)
    ]

    def test_list_users_without_params_response_code(self):
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        Assertions.assert_code_status(list_users_response, 200)

    def test_list_users_with_page_response_code(self):
        params = {
            'page': 2,
        }
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}', params=params)
        Assertions.assert_code_status(list_users_response, 200)

    def test_list_users_with_delay_response_code(self):
        params = {
            'delay': 3,
        }
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}', params=params)
        Assertions.assert_code_status(list_users_response, 200)

    @pytest.mark.parametrize('test_delay_time', delay_params)
    def test_list_users_with_delay_response_time(self, test_delay_time):
        params = {
            'delay': test_delay_time,
        }
        start = time.time()
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}', params=params)
        end = int(time.time() - start)
        assert end == test_delay_time, f'expected delay time {test_delay_time} second, but delay is {end}'

    def test_list_users_has_response_fields(self):
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        expected_fields = ['page', 'per_page', 'total', 'total_pages', 'data']
        Assertions.assert_json_value_has_keys(list_users_response, expected_fields)

    def test_list_users_data_field_len(self):
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        len_data_field = len(self.get_json_value(list_users_response, 'data'))
        per_page = self.get_json_value(list_users_response, 'per_page')
        assert len_data_field == per_page, f'expected len data field is {per_page}, but len is {len_data_field}'

    def test_list_users_data_field_has_fields(self):
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        expected_fields = ['id', 'email', 'first_name', 'last_name', 'avatar']
        data_fields = self.get_json_value(list_users_response, 'data')
        for data in data_fields:
            Assertions.assert_json_value_has_keys(data, expected_fields)

    def test_list_users_totat_field_value(self):
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        total_value = self.get_json_value(list_users_response, 'total')
        per_page = self.get_json_value(list_users_response, 'per_page')
        total_pages = self.get_json_value(list_users_response, 'total_pages')
        assert total_value == per_page * total_pages, f'expected total value is {per_page * total_pages},' \
                                                      f'but value is {total_value}'

    def test_list_users_empty_data_field(self):
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        total_pages = self.get_json_value(list_users_response, 'total_pages')
        params = {
            'page': total_pages + 1,
        }
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}', params=params)
        len_data_field = len(self.get_json_value(list_users_response, 'data'))
        assert len_data_field == 0, f'expected len data field is 0, but len is {len_data_field}'

    def test_list_users_avatar_field(self):
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\" \
                      "b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        data_fields = self.get_json_value(list_users_response, 'data')
        for data in data_fields:
            avatar = data['avatar']
            url_test = re.match(url_pattern, avatar)
            assert url_test, f'expected avatar in url format, but avatar is {avatar}'

    def test_list_users_email_field(self):
        email_pattern = r"^\S+@\S+\.\S+$"
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        data_fields = self.get_json_value(list_users_response, 'data')
        for data in data_fields:
            email = data['email']
            url_test = re.match(email_pattern, email)
            assert url_test, f'expected email in mail format, but email is {email}'

    def test_list_users_fields_type(self):
        example_fields = {
            "page": 2,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": [
                {
                    "id": 7,
                    "email": "michael.lawson@reqres.in",
                    "first_name": "Michael",
                    "last_name": "Lawson",
                    "avatar": "https://reqres.in/img/faces/7-image.jpg"
                },
            ],
            "support": {
                "url": "https://reqres.in/#support-heading",
                "text": "To keep ReqRes free, contributions towards server costs are appreciated!"
            }
        }
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        response_as_dict = list_users_response.json()
        for key, value in response_as_dict.items():
            expected_type = type(example_fields[key])
            assert type(value) == expected_type, f'expected {key} type is {expected_type}, but type is {type(value)}'

    def test_list_users_data_fields_type(self):
        example_fields = {
                    "id": 7,
                    "email": "michael.lawson@reqres.in",
                    "first_name": "Michael",
                    "last_name": "Lawson",
                    "avatar": "https://reqres.in/img/faces/7-image.jpg"
                }
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        data_field = self.get_json_value(list_users_response, 'data')
        for data in data_field:
            for key, value in data.items():
                expected_type = type(example_fields[key])
                assert type(value) == expected_type, f'expected {key} type is {expected_type}, ' \
                                                     f'but type is {type(value)}'

    def test_list_users_support_fields_type(self):
        example_fields = {
                "url": "https://reqres.in/#support-heading",
                "text": "To keep ReqRes free, contributions towards server costs are appreciated!"
                }
        list_users_response = requests.get(f'{self.BASE_URL}{self.LIST_USERS_URL}')
        support = self.get_json_value(list_users_response, 'support')
        for key, value in support.items():
            expected_type = type(example_fields[key])
            assert type(value) == expected_type, f'expected {key} type is {expected_type}, but type is {type(value)}'