from pydantic import BaseModel

class TideChangeResponse(BaseModel):
    time: str
    level: float
    type: str

class TideMessageResponse(BaseModel):
    state: str
    port_id: str
    current_time: str
    next_tide_change: TideChangeResponse
    message: str
