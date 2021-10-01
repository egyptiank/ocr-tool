from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.templating import Jinja2Templates
import shutil
import os
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/v1/extract_text")
async def extract_text(image: UploadFile = File(...)):
    temp_file = _save_file_to_disk(image, path="temp", save_as="temp")
    text = await colorize(temp_file)
    return {"filename": image.filename, "text": text}


def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


async def colorize(path):
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={
            'image': open(path, 'rb'),
        },
        headers={'api-key': '3a1506b8-06bd-44a2-9bdf-305964d21330'}
    )

    res = 'https:'+str(r.json()).split(':')[-1]
    return res[:len(res)-2]
