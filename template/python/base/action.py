import sentry


def input(body, key):
    return body['input'][key]


def hasura(body, key):
    hasura_key = f'x-hasura-{key}'
    session = body['session_variables']
    return session[hasura_key] if hasura_key in session else 'none'


def configure_sentry(body, **tags):
    tags['app.action'] = body['action']['name']
    sentry.configure(body, **tags)
