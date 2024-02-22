from enum import Enum

import pyautogui
from fastapi import FastAPI
from ruamel.yaml import YAML

import os

# Read allowed keys
yaml = YAML()
config_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "config.yaml",
    )
with open(config_file, "r") as stream:
    read = yaml.load(stream)
mapping = {key: key for key in read["allowed_keys"]}
AvailKeys = Enum("AvailKeys", mapping)

# Define endpoints
app = FastAPI()


@app.get("/{key}")
async def get_stroke(key: AvailKeys):
    pyautogui.keyDown(key.value)
    return {"message": f"Pressed {key.value}!"}
