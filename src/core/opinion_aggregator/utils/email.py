"""Contains email management functionality."""
from django.core.mail import EmailMultiAlternatives


def send_email(subject, from_email, to, message, html_content=None):
    """
    Send an email to the company.
    """
    to_email = to
    subject = subject
    subject = ''.join(subject.splitlines())
    body = message
    email_message = EmailMultiAlternatives(subject, body, None, [to_email])
    email_message.content_subtype = "html"
    email_message.send()

    # msg = EmailMultiAlternatives(subject, message, from_email, [to])
    # if html_content:
    #     msg.attach_alternative(html_content, "text/html")
    # msg.send()