from pydantic import BaseModel

class FlagsRead(BaseModel):
    maximum_risk_percentage : float | None = None
    default_risk_percentage : float | None = None
    total_balance : float | None = None