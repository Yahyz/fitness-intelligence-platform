from app.models.identity.user import User


def build_user(
    email: str,
    password_hash: str,
) -> User:
    return User(
        email=email.lower(),
        password_hash=password_hash,
        is_active=True,
        is_verified=False,
    )