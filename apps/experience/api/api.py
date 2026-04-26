from fastapi import APIRouter, Depends, HTTPException

from apps.experience.api_schema import (
    ExperienceRead,
    ExperienceCreate,
    ExperienceUpdate
)
from apps.experience.repository import ExperienceRepository

experience_api = APIRouter(prefix="/experience", tags=["Experience"])


@experience_api.post("/create_one", response_model=ExperienceRead)
async def create_one(
    experience_create: ExperienceCreate,
    repo: ExperienceRepository = Depends()
):
    result = await repo.create_one(experience_create.to_experience())
    return result


@experience_api.get("/read_one/{id}", response_model=ExperienceRead)
async def read_one(
    id: int,
    repo: ExperienceRepository = Depends()
):
    result = await repo.read_one(id)

    return result


@experience_api.get("/read_many", response_model=list[ExperienceRead])
async def read_many(
    repo: ExperienceRepository = Depends()
):
    result = await repo.read_many()
    return result


@experience_api.put("/update", response_model=ExperienceRead)
async def update(
    experience_update: ExperienceUpdate,
    repo: ExperienceRepository = Depends()
):
    experience = await repo.read_one(experience_update.id)

    if experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    if experience_update.note is not None:
        experience.note = experience_update.note

    updated = await repo.update(experience)

    return updated

