from rest_framework.exceptions import APIException


class HttpPaymentException(APIException):
    status_code = 400
