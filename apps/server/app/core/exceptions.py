class EmailAlreadyExistsError(Exception):
    """Raised when attempting to register with an existing email."""


class RoleNotFoundError(Exception):
    """Raised when a required role does not exist."""


class OrganizationAlreadyExistsError(Exception):
    """Raised when an organization slug already exists."""