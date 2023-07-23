from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        'validationError': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
        'Unauthorized': _handle_authentication_error,
        'AuthenticationFailed': _handle_authentication_error,
        'InvalidToken': _handle_invalidtoken_error,
        'NotAcceptable': _handle_authentication_error,
    }
    response = exception_handler(exc, context)
    if response is not None:
        response.data['code'] = response.status_code
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_authentication_error(exc, context, response):
    response.data = {
        'message': 'No authentication provided',
        'code': response.status_code
    }
    return response


def _handle_generic_error(exc, context, response):
    response.data = {
        'message': 'Permission denied!.',
        'code': response.status_code
    }
    return response


def _handle_invalidtoken_error(exc, context, response):
    response.data = {
        'message': 'Invalid authentication token.',
        'code': response.status_code
    }
    return response
