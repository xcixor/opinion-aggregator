"""Contains email management functionality."""
from django.core.mail import EmailMultiAlternatives


def send_email(subject, from_email, to, message, html_content=None):
    """
    Send an email to the company.
    """
    msg = EmailMultiAlternatives(subject, message, from_email, [to])
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    msg.send()