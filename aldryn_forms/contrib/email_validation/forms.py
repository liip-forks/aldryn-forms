from aldryn_forms.forms import FormSubmissionBaseForm

from .models import EmailValidationFormSubmission


class EmailValidationFormSubmissionBaseForm(FormSubmissionBaseForm):

    def __init__(self, *args, **kwargs):
        super(EmailValidationFormSubmissionBaseForm, self).__init__(*args, **kwargs)
        language = self.form_plugin.language

        self.instance = EmailValidationFormSubmission(
            name=self.form_plugin.name,
            language=language,
            form_url=self.request.build_absolute_uri(self.request.path),
        )
