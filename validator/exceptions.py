from rest_framework import status
from rest_framework.exceptions import APIException


class NotFoundRequestException(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class ForbiddenRequestException(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class InvalidTimeRangeRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class EmptyTagException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class EmptyTagException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidFiltersException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST