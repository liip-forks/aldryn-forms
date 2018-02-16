from django.core import signing
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import EmailValidationFormSubmission


def validate_email(request, token):
    signer = signing.Signer()
    try:
        unsigned_token = signer.unsign(token)
    except signing.BadSignature:
        return HttpResponseBadRequest()

    form_pk, email = unsigned_token.split('-')

    form_submission = get_object_or_404(EmailValidationFormSubmission, pk=int(form_pk))
    form_submission.is_valid = True
    form_submission.save()

    # TODO: render template
    return HttpResponse("Validated")
