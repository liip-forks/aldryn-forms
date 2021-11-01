from django.contrib import admin

from aldryn_forms.admin import FormSubmissionAdmin

from .models import EmailValidationFormSubmission, ValidatedEmail


class ValidatedFormSubmissionAdmin(FormSubmissionAdmin):
    list_display = ['__str__', 'sent_at', 'language', 'is_valid']
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


class ValidatedEmailAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


admin.site.register(EmailValidationFormSubmission, ValidatedFormSubmissionAdmin)
admin.site.register(ValidatedEmail, ValidatedEmailAdmin)
