import os
from sentry_sdk import configure_scope


def configure(user_id, role, **tags):
    with configure_scope() as scope:
        scope.user = {'id': user_id}
        scope.set_tag('user.role', role)

        app = os.environ.get('APP_NAME', 'unknown')
        scope.set_tag('app.name', app)

        for tag, value in tags.items():
            scope.set_tag(tag, value)
