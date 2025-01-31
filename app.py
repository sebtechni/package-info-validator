import os
import sys
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import APIRouter, Request, Form, FastAPI, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.params import Query
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


@app.post("/upload-htmx/", response_class=HTMLResponse)
async def upload_files_htmx(files: List[UploadFile] = File(...)):
    file_rows = ""

    for file in files:
        size_kb = round(len(await file.read()) / 1024, 2)
        file_rows += f"""
        <tr class="hover:bg-gray-100 transition">
            <td class="py-2 px-4">{file.filename}</td>
            <td class="py-2 px-4">{file.content_type}</td>
            <td class="py-2 px-4">{size_kb} KB</td>
        </tr>
        """

    return file_rows  # HTMX dynamically updates the table