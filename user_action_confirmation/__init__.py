# major, minor, patch
VERSION = (0, 1, 3)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    return version


def create_ticket(action, user=None):
    from user_action_confirmation.models import Confirmation
    return Confirmation.objects.create(user=user, action=action).token
