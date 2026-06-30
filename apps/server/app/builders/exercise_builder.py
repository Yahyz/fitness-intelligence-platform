from app.models.exercises.exercise import Exercise


def build_exercise(
    *,
    organization_id,
    created_by,
    name,
    slug,
    description,
    instructions,
    difficulty,
    movement_pattern,
    video_url,
    thumbnail_url,
):

    return Exercise(
        organization_id=organization_id,
        created_by=created_by,
        name=name,
        slug=slug,
        description=description,
        instructions=instructions,
        difficulty=difficulty,
        movement_pattern=movement_pattern,
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        is_system=False,
        is_active=True,
    )