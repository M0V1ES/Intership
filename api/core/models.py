from typing import Optional

from pydantic import BaseModel, constr


class SMSRequest(BaseModel):
    sender: Optional[constr(min_length=11, max_length=11)]
    recipient: Optional[constr(min_length=11, max_length=11)]
    message: Optional[constr(min_length=1, max_length=300)]


class SMSResponse(BaseModel):
    status_code: int
    message: str
