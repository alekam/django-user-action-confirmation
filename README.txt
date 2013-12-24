
django-user-action-confirmation
===============================


Overview
~~~~~~~~

Easy and simple way to confirm user actions.
This one can be used with email or sms confirmation, but not provide this functional.


Installation
~~~~~~~~~~~~

Install developer version using PIP::

    pip install -e git+https://github.com/alekam/django-user-action-confirmation#egg=user_action_confirmation

Change ``settings.py`` of your project. Add ``user_action_confirmation`` to
``INSTALLED_APPS``. Add required options (see: Settings).

Run ``manage.py syncdb`` or ``manage.py migrate options`` if you use South
and restart your project server.


Settings
~~~~~~~~

CONFIRMATION_OPERATION_CHOICES - required, list of tuples witch contains operation ID and short description

CONFIRMATION_MAX_DAYS - optional, default is 3 days


Usage
~~~~~

Install it, plug-in to your project and add required settings. Have fun!


Usage example (somethere in FormView.form_valid):

    name = sa_setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY',
                      'partial_pipeline')
    backend = self.request.session[name]['backend']
    email = form.cleaned_data['email']

    token = Confirmation.objects.create(None, settings.OPERATION_REGISTER)
    token.params = {
        'email': email,
        'backend': backend
    }
    token.save()

    mail.send(
        [email, ],
        settings.DEFAULT_FROM_EMAIL,
        template='confirm_registration',
        context={
            'user': {
                'first_name': self.request.session.get('saved_first_name', '')
            },
            'site': Site.objects.get_current(),
            'token': token.token,
            'confirm_url': reverse('auth_confirm_email',
                                   args=[token.token, ])
        }
    )


Provided template tags and libraries
~~~~~~~~~~~~~~~~~~~~~~~

No any templeate tags provided


Provided management commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No any management commands provided


Testing
~~~~~~~

If this application is installed in your project you can run this inside your
project::

    python manage.py test user_action_confirmation

or instead run inside this package::

    python run_tests.py

