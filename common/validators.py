from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def mobile_validator(mobile):
    if mobile[0:2] != '09':
        raise ValidationError('Please follow the mentioned format')


def mobile_length_validator(mobile):
    if len(mobile) != 11:
        raise ValidationError('Please follow the mentioned format:invalid length')


FARSI_LANGUAGE = RegexValidator("^[\u0600-\u06FF\s]+$")
EN_LANGUAGE = RegexValidator("^[a-zA-Z\s]+$")
