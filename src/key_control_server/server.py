from enum import Enum

import pyautogui
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ruamel.yaml import YAML

from key_control_server.globals import config_file

# Read allowed keys
yaml = YAML()

with open(config_file, "r") as stream:
    read = yaml.load(stream)
mapping = {key: key for key in read["allowed_keys"]}
AvailKeys = Enum("AvailKeys", mapping)

# Define endpoints
app = FastAPI()

@app.get("/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/{key}")
async def get_stroke(key: AvailKeys):
    pyautogui.keyDown(key.value)
    return {"message": f"Pressed {key.value}!"}
