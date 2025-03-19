from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from api.core.models import SMSRequest

app = FastAPI()
security = HTTPBasic()


@app.post("/send_sms")
def sms_send(
    sms: SMSRequest, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return sms


if __name__ == "__main__":
    uvicorn.run(app, port=4010)
