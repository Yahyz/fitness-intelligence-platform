import uuid

from app.models.identity.client_profile import ClientProfile
from app.models.identity.coach_profile import CoachProfile


def build_coach_profile(
    user_id: uuid.UUID,
    first_name: str,
    last_name: str,
    phone: str | None = None,
) -> CoachProfile:
    return CoachProfile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )


def build_client_profile(
    user_id: uuid.UUID,
    first_name: str,
    last_name: str,
    phone: str | None = None,
) -> ClientProfile:
    return ClientProfile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )