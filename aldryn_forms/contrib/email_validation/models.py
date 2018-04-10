from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_forms.models import FormPlugin, FormSubmission


class EmailValidationFormPlugin(FormPlugin):

    class Meta:
        proxy = True


class EmailValidationFormSubmission(FormSubmission):
    is_valid = models.BooleanField(
        verbose_name=_('is valid'),
        default=False
    )

    class Meta:
        verbose_name = _('Form submission with validated email')
        verbose_name_plural = _('Form submissions with validated email')


class ValidatedEmail(models.Model):
    email = models.EmailField(
        verbose_name=_('Email'),
        null=True,
        blank=True,
        unique=True
    )
    date = models.DateField(
        verbose_name=_('Date'),
        auto_now=True
    )
    form_submission = models.ForeignKey(
        'EmailValidationFormSubmission',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Validated email')
        verbose_name_plural = _('Validated emails')
