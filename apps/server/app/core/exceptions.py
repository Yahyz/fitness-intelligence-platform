class EmailAlreadyExistsError(Exception):
    """Raised when attempting to register with an existing email."""


class RoleNotFoundError(Exception):
    """Raised when a required role does not exist."""


class OrganizationAlreadyExistsError(Exception):
    """Raised when an organization slug already exists."""

class InvalidCredentialsError(Exception):
    """Raised when the email or password is invalid."""


class InactiveUserError(Exception):
    """Raised when a user account is inactive."""

class ClientAlreadyExistsError(Exception):
    """Raised when a client email already exists."""


class ClientRoleNotFoundError(Exception):
    """Raised when the Client role is missing."""