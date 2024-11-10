from datetime import datetime
import re
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


def is_numeric(txt):
    if txt is None or txt == '':
        return False
    if type(txt) is int:
        return True
    return True if txt.isdigit() else False


def is_date(date: str, date_format='%m-%d-%Y'):
    """
    takes a string and returns true if the string is a date
    """

    try:
        datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def is_url(url):
    # Regular expression for URL validation
    url_pattern = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https:// or ftp://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)

    return bool(re.match(url_pattern, url))


def is_email(email_address):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(email_regex, email_address):
        return True
    else:
        return False


def is_strong_password(
        password: str,
        min_len: int = 8,
        max_len: int = 50,
        use_letters: bool = True,
        use_digits: bool = True
):
    """
    Takes a string and checks if it is an appropriate password or not.
    """

    if password is None:
        return False
    if (len(password) < min_len) or (len(password) > max_len):
        return False
    letter_flag = not use_letters
    digit_flag = not use_digits
    for char in password:
        if char.isdigit():
            digit_flag = True
        elif char.isalpha():
            letter_flag = True
    return letter_flag and digit_flag


def is_iran_mobile(phone):
    """
    takes a string then if it is a valid iran mobile phone returns true else false
    """
    if phone is None or phone == '':
        return False
    if is_numeric(phone):
        int_phone = int(phone)
    else:
        return False

    phone_regex = r'09(\d{9})$'

    if (phone[0] != '0' or phone[1] != '9') and (phone[0] != '۰' or phone[1] != '۹'):
        return False
    if re.fullmatch(phone_regex, '0' + str(int_phone)):
        return True
    else:
        return False


def is_only_alphabet_and_space(name: str, english: bool = True, persian: bool = True, minlength: int = 2,
                               maxlength: int = 50) -> bool:
    """
    if the string is only contained alphabet and space returns True else => false
    """

    english_name_regex = r"^[A-Za-z\-'\s]+$"
    persian_name_regex = r"^[\u0600-\u06FF\s]+$"

    if not name:
        return False
    if len(name) > maxlength or len(name) < minlength:
        return False
    # the name cannot be english and persian at same time
    per_check = True
    eng_check = True
    if persian:
        if not re.fullmatch(persian_name_regex, name):
            per_check = False
    if english:
        if not re.fullmatch(english_name_regex, name):
            eng_check = False
    if persian and not per_check and not english:
        return False
    if english and not eng_check and not persian:
        return False

    if persian and english:
        if not (per_check != eng_check):
            return False
    return True


def validate_location(value):
    # Regular expression to match a comma-separated latitude and longitude
    pattern = re.compile(r'^-?\d{1,3}\.\d+,-?\d{1,3}\.\d+$')
    if not pattern.match(value):
        raise ValidationError(f"{value} is not a valid location format")

    # Split the string to get latitude and longitude
    lat_str, lon_str = value.split(',')
    latitude = float(lat_str)
    longitude = float(lon_str)

    # Check if latitude and longitude are within valid ranges
    if not (-90 <= latitude <= 90):
        raise ValidationError(f"Latitude {latitude} is out of range (-90 to 90)")
    if not (-180 <= longitude <= 180):
        raise ValidationError(f"Longitude {longitude} is out of range (-180 to 180)")
