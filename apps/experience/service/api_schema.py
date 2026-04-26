from datetime import datetime
from pydantic import BaseModel, ConfigDict

from apps.experience.data.models import Experience


class ExperienceCreate(BaseModel):
    note: str

    def to_experience(self) -> Experience:
        return Experience(
            note = self.note
        )

class ExperienceUpdate(BaseModel):
    id : int
    note: str | None = None

class ExperienceRead(BaseModel):
    id: int
    note: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
