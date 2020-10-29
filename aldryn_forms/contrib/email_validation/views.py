import ast
import json

from django.core import signing
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.db import transaction

from emailit.api import send_mail

from .models import EmailValidationFormSubmission, ValidatedEmail


def validate_email(request, token):
    signer = signing.Signer()
    try:
        unsigned_token = signer.unsign(token)
    except signing.BadSignature:
        return HttpResponseBadRequest()

    form_pk, email = unsigned_token.split('-', 1)
    with transaction.atomic():
        form_submission = get_object_or_404(EmailValidationFormSubmission, pk=int(form_pk))
        if not form_submission.is_valid:
            form_submission.is_valid = True
            form_submission.save()

            validated_email = ValidatedEmail.objects.get_or_create(
                email=email,
                form_submission=form_submission
            )
            validated_email.save()

            notification_context = {
                'form_name': form_submission.name,
                'form_data': ast.literal_eval(form_submission.data),
                'form_plugin': form_submission,
            }

            recipients = json.loads(form_submission.recipients)

            send_mail(
                recipients=[user['email'] for user in recipients],
                context=notification_context,
                template_base='email_validation/emails/notification',
                language=form_submission.language,
            )

    context = {
        'email': email
    }

    return render(request, 'email_validation/validated.html', context)
