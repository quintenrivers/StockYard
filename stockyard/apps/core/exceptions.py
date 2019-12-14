from rest_framework.views import exception_handler


def core_exception_handler(exc, context) -> exception_handler.__class__:
    # Delegates exception to default exception handler offered by DRF
    # if not explicitly handled here
    response: exception_handler.__class__ = exception_handler(exc, context)
    handlers: dict = {
        'ValidationError': _handle_generic_error
    }

    exception_class: str = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response) -> dict:
    response.data: dict = {
        'errors': response.data
    }

    return response
