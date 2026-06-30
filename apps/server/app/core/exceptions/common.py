class ForbiddenError(Exception):
    """Raised when the user is not allowed to perform an action."""


class NotFoundError(Exception):
    """Raised when a resource cannot be found."""


class ValidationError(Exception):
    """Raised when validation fails."""