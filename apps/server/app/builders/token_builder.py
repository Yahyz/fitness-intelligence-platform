from datetime import datetime, timedelta

from app.core.config import settings
from app.models.identity.refresh_token import RefreshToken


def build_refresh_token(
    user_id,
    token: str,
) -> RefreshToken:
    return RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=datetime.utcnow()
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False,
    )