# coding: utf-8
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from jsonfield import JSONField
import datetime
import hashlib
import random


__all__ = ['Confirmation', ]


def create_token(email):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt + email.encode('utf8')).hexdigest()


class ConfirmationManager(models.Manager):

    def create(self, user, action):
        kwargs = {
            'user': user,
            'token': create_token(unicode(user)),
            'action': action
        }
        return super(ConfirmationManager, self).create(**kwargs)


class Confirmation(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=u'пользователь',
                             blank=True, null=True)
    created = models.DateTimeField(u'запрошено', auto_now_add=True)
    token = models.CharField(max_length=40, blank=True)
    action = models.PositiveSmallIntegerField(u'операция',
                        choices=settings.CONFIRMATION_OPERATION_CHOICES)
    confirmed = models.DateTimeField(u'подтверждено', blank=True, null=True)
    params = JSONField(u'доп.данные', blank=True, null=True)

    objects = ConfirmationManager()

    class Meta:
        verbose_name = u'подтверждение операции'
        verbose_name_plural = u'подтверждение операций'

    def __unicode__(self):
        return self.token

    def is_valid(self):
        return (datetime.datetime.now() - self.created).days < \
                                    getattr(settings, 'CONFIRMATION_MAX_DAYS', 3)
    is_valid.boolean = True
    is_valid.short_description = u'актуален'

    def is_expired(self):
        return not self.is_valid()
    is_expired.boolean = True
    is_expired.short_description = u'просрочен'

    def is_confirmed(self):
        return self.confirmed is not None
    is_confirmed.boolean = True
    is_confirmed.short_description = u'подтвержден'

    def confirm(self):
        self.confirmed = datetime.datetime.now()
        self.save()
