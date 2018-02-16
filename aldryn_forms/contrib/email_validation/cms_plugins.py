import logging

from django.utils.translation import ugettext_lazy as _

from aldryn_forms.cms_plugins import FormPlugin
from aldryn_forms.helpers import get_user_name
from aldryn_forms.validators import is_valid_recipient
from cms.plugin_pool import plugin_pool

from .forms import EmailValidationFormSubmissionBaseForm
from .models import EmailValidationFormPlugin

logger = logging.getLogger(__name__)


class EmailValidationForm(FormPlugin):
    name = _('Form (Email validation)')
    model = EmailValidationFormPlugin

    def form_valid(self, instance, request, form):
        form.instance.set_recipients(self.get_recipients(instance, form))
        form.save()

    def get_recipients(self, instance, form):
        users = instance.recipients.exclude(email='')

        recipients = [user for user in users.iterator()
                      if is_valid_recipient(user.email)]

        users_to_notify = [
            (get_user_name(user), user.email) for user in recipients]
        return users_to_notify

    def get_form_class(self, instance):
        """
        Constructs form class basing on children plugin instances.
        """
        fields = self.get_form_fields(instance)
        formClass = (
            type(EmailValidationFormSubmissionBaseForm)
            ('AldrynDynamicForm', (EmailValidationFormSubmissionBaseForm,), fields)
        )
        return formClass


plugin_pool.register_plugin(EmailValidationForm)
