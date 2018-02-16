from django.contrib import admin
from django.utils import six

from aldryn_forms.admin import FormSubmissionAdmin

from .models import EmailValidationFormSubmission

if six.PY2:
    str_dunder_method = '__unicode__'
else:
    str_dunder_method = '__str__'


class ValidatedFormSubmissionAdmin(FormSubmissionAdmin):
    list_display = [str_dunder_method, 'sent_at', 'language', 'is_valid']
    readonly_fields = [
        'name',
        'get_data_for_display',
        'language',
        'sent_at',
        'get_recipients_for_display',
        'is_valid',
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_valid=True)


admin.site.register(EmailValidationFormSubmission, ValidatedFormSubmissionAdmin)
