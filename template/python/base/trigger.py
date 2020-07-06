import sentry


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
    tags['app.trigger'] = body['trigger']['name']
    sentry.configure(body, **tags)
