from django.core.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db.models.deletion import ProtectedError

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    # Handle ProtectedError (foreign key constraint)
    if isinstance(exc, ProtectedError):
        return Response(
            {
                'detail': 'Cannot delete this item because it is referenced by other records.',
                'error_code': 'protected_error',
                'protected_objects': str(exc.protected_objects)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

    if isinstance(exc, ValidationError):
        # ValidationError can have different formats
        if hasattr(exc, 'message_dict'):
            # Field-specific errors: {'field': ['error1', 'error2']}
            return Response(exc.message_dict, status=status.HTTP_400_BAD_REQUEST)
        elif hasattr(exc, 'messages'):
            # List of error messages
            return Response(
                {
                    'detail': exc.messages[0] if exc.messages else 'Validation error',
                    'error_code': 'validation_error'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Fallback
            return Response(
                {
                    'detail': str(exc),
                    'error_code': 'validation_error'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    return response