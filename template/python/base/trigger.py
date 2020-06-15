def data(body, key=None):
    if key:
        return body['event']['data']['new'][key]
    else:
        return body['event']['data']


def hasura(body, key):
    hasura_key = f'x-hasura-{key}'
    return body['event']['session_variables'][hasura_key]
