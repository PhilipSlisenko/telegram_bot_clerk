import functools
from config import config
import requests


def guarantee_token(f):
    """ Guaranties that token is in context.user_data['token']. 
    Gets token from API if it is not already stored in context.user_data['token'] """
    @functools.wraps(f)
    def inner(update, context):
        if not context.user_data.get('token'):
            username = update.effective_user.full_name
            telegram_id = update.effective_user.id
            url = config['api_url'] + '/clerks/register-and-login'
            payload = {
                "username": username,
                "password": str(username) + str(telegram_id),
                "telegram_id": telegram_id
            }
            res_json = requests.post(url, json=payload).json()
            context.user_data['token'] = res_json.get('token')
            context.user_data['username'] = username
            return f(update, context)
    return inner