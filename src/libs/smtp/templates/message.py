from .base import template


def send_mail(body):
    return template(body=body)