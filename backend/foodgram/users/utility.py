import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# from django.utils.regex_helper import _lazy_re_compile


username_validator = RegexValidator(
    re.compile('^[\w.@+-]+\Z'),
    message='Введите корректное имя пользователя.',
    code='invalid',
)


def username_is_valid(username):
    try:
        username_validator(username)
        return True
    except ValidationError:
        return False
