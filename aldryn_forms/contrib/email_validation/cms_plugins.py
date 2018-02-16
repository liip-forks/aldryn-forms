import logging

from django.core.signing import Signer
from django.utils.translation import ugettext_lazy as _

from aldryn_forms.cms_plugins import FormPlugin
from aldryn_forms.helpers import get_user_name
from aldryn_forms.validators import is_valid_recipient
from cms.plugin_pool import plugin_pool
from emailit.api import send_mail

from .forms import EmailValidationFormSubmissionBaseForm
from .models import EmailValidationFormPlugin

logger = logging.getLogger(__name__)


class EmailValidationForm(FormPlugin):
    name = _('Form (Email validation)')
    model = EmailValidationFormPlugin
    email_to_validate = None
    key_salt = "aldryn_forms.contrib.email_validation.EmailValidationForm"

    def form_valid(self, instance, request, form):
        form.instance.set_recipients(self.get_recipients(instance, form))
        form.save()
        self.send_validation_email(instance, form)

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

    def send_validation_email(self, instance, form):
        self.email_to_validate = self.get_form_email(form)

        if not self.email_to_validate:
            return

        context = {
            'form_name': instance.name,
            'form_data': form.get_serialized_field_choices(),
            'form_plugin': instance,
            'validation_link': self.generate_validation_link(instance, form),
        }

        send_mail(
            recipients=self.email_to_validate,
            context=context,
            template_base='email_validation/emails/validation',
            language=instance.language
        )

    def get_form_email(self, form):
        email_fields = [(name, field) for name, field in form.fields.items()
                       if field.__class__.__name__ == 'EmailField']
        if len(email_fields) == 0:
            return None

        email_field_name = email_fields[0][0]
        return form.data[email_field_name]

    def generate_validation_link(self, instance, form):
        signer = Signer()

        token = '{}-{}'.format(str(form.instance.pk), self.email_to_validate)

        signed_token = signer.sign(token)

        return signed_token


plugin_pool.register_plugin(EmailValidationForm)
