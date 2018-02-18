from django.conf.urls import url

from .views import validate_email

urlpatterns = [
    url(r'^validate/(?P<token>.+)/$', validate_email, name='email_validation_validate_email'),
]
