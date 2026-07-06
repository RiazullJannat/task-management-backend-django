from rest_framework.views import exception_handler
from rest_framework import status
from .response_utils import error_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return error_response(
            'Internal server error',
            {'detail': str(exc)},
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(response.data, dict) and 'detail' in response.data:
        message = response.data['detail']
        errors = {'detail': message}
    else:
        message = 'Request failed'
        errors = response.data

    return error_response(message, errors, response.status_code)
