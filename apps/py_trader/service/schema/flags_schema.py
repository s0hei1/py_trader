from pydantic import BaseModel, ConfigDict


class FlagsRead(BaseModel):
    is_first_run : bool
    is_development : bool

    model_config = ConfigDict(from_attributes=True)
