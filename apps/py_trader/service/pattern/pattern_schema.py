from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class PatternGroupRead(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class PatternGroupCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    is_active: bool = True
