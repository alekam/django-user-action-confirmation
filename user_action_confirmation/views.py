# coding: utf-8
from .models import Confirmation
from django.core.validators import EMPTY_VALUES
from django.http.response import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.views.generic.base import TemplateView


__all__ = ['ConfirmActionView', ]


class ConfirmActionView(TemplateView):
    '''Base view to confirm actions'''
    token = None
    success_url = None
    operation = None
    error_messages = {
        'missing': u'Ссылка не действительна.',
        'expired': u'Ссылка для подтверждения действия устарела.',
        'confirmed': u'Данное действия уже было подтверждено ранее.',
    }
    check_expiration = True
    redirect_field_name = 'next'
    token_field_name = 'token'

    def get(self, request, *args, **kwargs):
        key = self.kwargs.get(self.token_field_name, '').strip()
        self.error_message = False
        if key not in EMPTY_VALUES:
            try:
                token = Confirmation.objects.get(token=key,
                                             action=self.operation)
            except Confirmation.DoesNotExist:
                self.error_message = self.error_messages.get('missing')
                token = None

            if token is not None:
                if self.check_expiration and token.is_expired():
                    self.error_message = self.error_messages.get('expired')
                elif token.is_confirmed():
                    self.error_message = self.error_messages.get('confirmed')

            if not self.error_message:
                return self.token_valid(token)

        return TemplateView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = TemplateView.get_context_data(self, **kwargs)
        ctx.update({
            'error': self.error_message
        })
        return ctx

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(self.success_url)
        return redirect_to

    def token_valid(self, token):
        return HttpResponseRedirect(self.get_success_url())
