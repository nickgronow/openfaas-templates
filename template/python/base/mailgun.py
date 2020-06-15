import requests
import json


def send(**options):
    '''Send an email based on a Mailgun template.

    Returns a Response object.

    Required keyword arguments:
    domain -- String - The mailgun domain name
    apikey -- String - Api key to access mailgun's api
    from -- String - "name <name@domain.com>"
    to -- String - "name <name@domain.com>"
    subject -- String - Email subject
    template -- String - template slug
    variables -- Dictionary - variables used in the template
    '''
    return requests.post(
        f'https://api.mailgun.net/v3/{options["domain"]}/messages',
        auth=("api", options['apikey']),
        data={
            'from': options['from'],
            'to': options['to'],
            'subject': options['subject'],
            'template': options['template'],
            'h:X-Mailgun-Variables': json.dumps(options['variables'])
        }
    )
