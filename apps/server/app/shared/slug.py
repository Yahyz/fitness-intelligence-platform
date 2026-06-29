import re

from app.modules.auth.repository import AuthRepository


def slugify(value: str) -> str:
    value = value.lower().strip()

    value = re.sub(r"[^\w\s-]", "", value)

    value = re.sub(r"[-\s]+", "-", value)

    return value


def generate_unique_slug(
    name: str,
    repository: AuthRepository,
) -> str:

    base = slugify(name)

    slug = base

    counter = 1

    while repository.slug_exists(slug):
        slug = f"{base}-{counter}"
        counter += 1

    return slug