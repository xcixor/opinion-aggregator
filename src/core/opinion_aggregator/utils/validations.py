"""Contains custom validators."""
import re
from django.forms import ValidationError


def clean_value(value, field):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if (regex.search(value) == None):
        return value
    else:
        raise  ValidationError(
    "{} cannot contain characters such as @#'%$& or !".format(field)
    )