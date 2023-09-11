from django.urls import re_path

from .views import validate_email

urlpatterns = [
    re_path(r'^validate/(?P<token>.+)/$', validate_email, name='email_validation_validate_email'),
]
