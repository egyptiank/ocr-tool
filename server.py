from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.templating import Jinja2Templates
import shutil
import os
import requests
import base64

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
    data = ""
    with open(path, "rb") as image_file:
        data = base64.encodestring(image_file.read())
    data = "data:image/"+ path.split('.')[1] + ";base64," + data
    r = requests.post(url='https://hf.space/gradioiframe/akhaliq/Real-ESRGAN/api/predict', json={"data": [data]})
    new_data = r.json().get("data")[0]
    res = new_data.replace('data:image/jpg;base64,','')
    res = base64.decodestring(new_data)
    #with open("imageToSave.png", "wb") as fh:
    #    fh.write(base64.decodebytes(res))
    return res
