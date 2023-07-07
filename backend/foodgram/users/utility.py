import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

username_validator = RegexValidator(
    re.compile(r'^[\w.@+-]+\Z'),
    message='Введите корректное имя пользователя.',
    code='invalid',
)


def username_is_valid(username):
    try:
        username_validator(username)
        return True
    except ValidationError:
        return False
