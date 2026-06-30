from .auth import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InactiveUserError,
    RoleNotFoundError,
)

from .clients import (
    ClientAlreadyExistsError,
    ClientRoleNotFoundError,
    ClientNotFoundError,
)

from .common import (
    ForbiddenError,
    NotFoundError,
    ValidationError,
)

__all__ = [
    "EmailAlreadyExistsError",
    "InvalidCredentialsError",
    "InactiveUserError",
    "RoleNotFoundError",
    "ClientAlreadyExistsError",
    "ClientRoleNotFoundError",
    "ClientNotFoundError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
]