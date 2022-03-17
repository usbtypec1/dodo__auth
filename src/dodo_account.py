from typing import Iterable

import requests

import config
import exceptions
import redis_db
import utils

__all__ = (
    'DodoAccount',
    'filter_accounts_with_expired_cookies',
    'get_dodo_accounts',
)


class DodoAccount:
    _login_url = 'https://auth.dodopizza.ru/Authenticate/LogOn'
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
    }
    __slots__ = ('__login', '__password', '__name')

    def __init__(self, name: str, login: str, password: str):
        self.__login = login
        self.__password = password
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def auth_data(self) -> dict:
        return {
            'CountryCode': 'Ru',
            'login': self.__login,
            'password': self.__password,
        }

    def get_auth_cookies(self) -> dict:
        with requests.Session() as session:
            response = session.post('https://auth.dodopizza.ru/Authenticate/LogOn',
                                    headers=self._headers, data=self.auth_data)
            if not response.ok:
                raise exceptions.UnsuccessfulAuthError
            return session.cookies.get_dict()


def filter_accounts_with_expired_cookies(accounts: Iterable[DodoAccount]):
    account_cookies_for_update = []
    for account in accounts:
        cookies_lifetime = redis_db.get_cookies_lifetime(account.name)
        if cookies_lifetime > config.COOKIES_UPDATE_THRESHOLD:
            continue
        account_cookies_for_update.append(account)
    return account_cookies_for_update


def get_dodo_accounts() -> list[DodoAccount]:
    credentials = utils.read_accounts_file()
    return [DodoAccount(account['name'], account['login'], account['password'])
            for account in credentials]