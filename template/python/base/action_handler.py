import os
from database import Database


class ActionHandler:
    """Common helper methods for Hasura Actions"""

    def __init__(self, event, context):
        self.body = event.body
        self.headers = event.headers
        self.namespace = os.environ.get('appname')
        self.secrets_path = (os.environ.get('secrets')
                             or '/var/openfaas/secrets')
        self.initialize_db()

    def initialize_db(self):
        if self.testing:
            return
        self.db = Database(
            host=self.secret('wov-db-host'),
            database=self.secret(f'{self.namespace}-db-name'),
            user=self.secret(f'{self.namespace}-db-user'),
            password=self.secret(f'{self.namespace}-db-pw')
        )

    def secret(self, name):
        path = f'{self.secrets_path}/{name}'
        with open(path, 'r') as file:
            return file.read()

    def log(self, message):
        if self.testing():
            return
        print(message)

    def testing(self):
        return os.environ.get('TESTING')

    def action(self):
        return self.body['action']['name']

    def input(self, key):
        return self.body['input'][key]

    def hasura(self, key):
        hasura_key = f'x-hasura-{key}'
        return self.body['session_variables'][hasura_key]

    def response(self, payload):
        return {
            'body': payload,
            'headers': {'content-type': 'application/json'},
            'code': 200
        }
