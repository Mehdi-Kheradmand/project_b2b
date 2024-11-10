from rest_framework import status
from rest_framework.exceptions import APIException


class TooManyRequests(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Request was throttled. Too many requests.'
    default_code = 'too_many_requests'
