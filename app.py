import os
import sys
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request, FastAPI, UploadFile, File
from fastapi.templating import Jinja2Templates
from typing import List

from validate import validate_yaml_schema

#uv run fastapi dev

app = FastAPI()

# Handle paths for PyInstaller
if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure FastAPI knows where to find templates
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def explore(request: Request):   

    return templates.TemplateResponse("index.html", {"request": request,
                                                      "id": id})

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    file_info = []

    for file in files:
        title, validation_info = await validate_yaml_schema(file)  # Await async function
        file_info.append({
            "filename": file.filename,
            "title": title,
            "validation_output": validation_info
        })

    return JSONResponse(content={"files": file_info})