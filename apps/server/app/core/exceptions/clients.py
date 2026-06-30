class ClientAlreadyExistsError(Exception):
    """Raised when a client email already exists."""


class ClientRoleNotFoundError(Exception):
    """Raised when the Client role cannot be found."""


class ClientNotFoundError(Exception):
    """Raised when a client does not exist."""