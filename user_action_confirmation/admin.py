from .models import *
from django.contrib import admin


class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'action', 'confirmed', 'is_valid']
    list_filter = ['action', 'created', ]


admin.site.register(Confirmation, ConfirmationAdmin)
