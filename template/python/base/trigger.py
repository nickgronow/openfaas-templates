from sentry_sdk import configure_scope


def data(body, key=None):
    if key:
        return body['event']['data']['new'][key]
    else:
        return body['event']['data']


def hasura(body, key):
    hasura_key = f'x-hasura-{key}'
    session = body['event']['session_variables']
    return session[hasura_key] if hasura_key in session else 'none'


def configure_sentry(body, **tags):
    with configure_scope() as scope:
        scope.user = {'id': hasura(body, 'user-id')}
        scope.set_tag('user.role', hasura(body, 'role'))

        for tag, value in tags.items():
            scope.set_tag(tag, value)

        scope.set_tag('trigger.name', body['trigger']['name'])
