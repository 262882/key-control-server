import os
from datetime import datetime
from enum import Enum

import pyautogui
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from ruamel.yaml import YAML

from key_control_server.globals import config_file, templates_path

# Read allowed keys
yaml = YAML()

with open(config_file, "r") as stream:
    read = yaml.load(stream)
mapping = {key: key for key in read["allowed_keys"]}
AvailKeys = Enum("AvailKeys", mapping)

# Prepare template
templates = Jinja2Templates(directory=templates_path)


# Set security
security = HTTPBasic()

def get_current_username(
        credentials: HTTPBasicCredentials = Depends(security)
        ):
    if credentials.password != os.environ["KEY_CONTROL_PASS"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Define endpoints
app = FastAPI(dependencies=[Depends(get_current_username)])

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="controls.html",
        context={
            "title": "Key-control-server",
            "keys": [[key, f"/{key}"] for key in mapping.keys()],
            }
    )


@app.get("/{key}")
async def get_stroke(key: AvailKeys):
    pyautogui.keyDown(key.value)
    return {
        "message": f"Pressed {key.value}!",
        "time": datetime.now(),
        }
