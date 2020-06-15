def name(body):
    return body['action']['name']


def input(body, key):
    return body['input'][key]


def hasura(body, key):
    hasura_key = f'x-hasura-{key}'
    return body['session_variables'][hasura_key]
