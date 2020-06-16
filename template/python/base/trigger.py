from sentry_sdk import configure_scope


def data(body, key=None):
    if key:
        return body['event']['data']['new'][key]
    else:
        return body['event']['data']


def hasura(body, key):
    hasura_key = f'x-hasura-{key}'
    return body['event']['session_variables'][hasura_key]


def configure_sentry(body, **tags):
    with configure_scope() as scope:
        scope.user = {'id': hasura('user-id')}

    for tag, value in tags.items():
        scope.set_tag(tag, value)
