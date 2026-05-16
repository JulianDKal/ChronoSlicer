from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from inspect_pdf import inspect_pdf

# from fastapi.params import File

router = APIRouter()

@router.post("/pdf_upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = Path("uploads")
    if(not file_path.exists()):
        file_path.mkdir(parents=True)
    file_path = file_path / file.filename

    print(f"Received file: {file.filename}, saving to: {file_path}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # inspect_pdf(file_path)
    return {"message": "PDF uploaded successfully", "filepath": file_path}