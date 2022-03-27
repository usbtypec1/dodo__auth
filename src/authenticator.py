import logging

import exceptions
import redis_db
from dodo_account import DodoAccount

__all__ = (
    'update_account_cookies',
)


def update_account_cookies(account: DodoAccount, repeat_times: int = 5):
    """Login in Dodo IS and save cookies in redis.

    Args:
        account: DodoAccount object.
        repeat_times: if auth request was unsuccessful, the request will be sent again.
    """
    try:
        cookies = account.get_auth_cookies()
        if not cookies:
            raise exceptions.UnsuccessfulAuthError
    except exceptions.UnsuccessfulAuthError:
        if repeat_times <= 0:
            logging.warning(f'Could not update account {account.name} cookies')
            return
        return update_account_cookies(account, repeat_times - 1)
    else:
        redis_db.set_cookies(account.name, cookies)
        logging.info(f'Account {account.name} cookies have been updated')
