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
