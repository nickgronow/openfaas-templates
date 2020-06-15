import base


def handle(event, context):
    base.log('PROCESSING')
    payload = {'status': 'success'}
    return base.response(payload)
