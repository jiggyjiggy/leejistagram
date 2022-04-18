import re

from users.models           import User

from django.core.exceptions import ValidationError

REGEX_EMAIL    = '^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$'


def validate_email(email):
    if not re.match(REGEX_EMAIL, email):
        raise ValidationError('INVALID_EMAIL', code=400)


def validate_password(password):
    if not re.search(REGEX_PASSWORD, password):
        raise ValidationError('INVALID_PASSWORD', code=400)


def exist_email(email):
    email_exist = User.objects.filter(email=email).exists()

    if email_exist:
        raise ValidationError('EXIST_EMAIL', code=400)

def match_user(email, password):
    email_exist    = User.objects.filter(email=email).exists()
    match_password = User.objects.filter(email=email, password=password).exists()

    if not email_exist or not match_password:
        raise ValidationError('INVALID_USER', code=401)

