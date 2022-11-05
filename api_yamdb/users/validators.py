import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            _(f'{value} служебное имя!')
        )
    if not re.match(r'[\w.@+-]+\Z', value):
        raise ValidationError(_(f'{value} содержит запрещенные символы!'))
