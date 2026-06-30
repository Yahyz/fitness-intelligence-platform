class EmailAlreadyExistsError(Exception):
    """Raised when an email is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when email or password is invalid."""


class InactiveUserError(Exception):
    """Raised when the user account is inactive."""


class RoleNotFoundError(Exception):
    """Raised when a required role cannot be found."""