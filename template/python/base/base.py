import os
from database import Database
import logging


def db():
    namespace = os.environ.get('APP_NAME')
    return Database(
        host=secret('wov-db-host'),
        database=secret(f'{namespace}-db-name'),
        user=secret(f'{namespace}-db-user'),
        password=secret(f'{namespace}-db-pw')
    )


def secret(name):
    path = os.environ.get('secrets') or '/var/openfaas/secrets'
    fullpath = f'{path}/{name}'
    with open(fullpath, 'r') as file:
        return file.read().rstrip('\n')


def log(message):
    if testing():
        return
    logging.info(message)


def testing():
    return os.environ.get('TESTING')


def production():
    return os.environ.get('APP_ENV') == 'production'


def response(payload):
    return {
        'body': payload,
        'headers': {'content-type': 'application/json'},
        'code': 200
    }
