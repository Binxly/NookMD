import os
import uuid
from typing import List

from fastapi import (APIRouter, Depends, File, HTTPException, Query,
                     UploadFile, status)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import PDF
from ..schemas import PDFListResponse, PDFResponse

router = APIRouter(prefix="/pdf", tags=["pdf"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

ALLOWED_MIME_TYPES = {"application/pdf"}


@router.post("/upload", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are allowed"
        )

    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_size = 0
        chunk_size = 1024 * 1024  # 1MB chunks

        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File size exceeds maximum limit of 50MB",
                )

        await file.seek(0)

        content = await file.read()
        secure_filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(UPLOAD_DIR, secure_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        db_pdf = PDF(filename=file.filename, path=file_path)
        db.add(db_pdf)
        db.commit()
        db.refresh(db_pdf)
        return db_pdf

    except HTTPException:
        raise
    except Exception as e:
        if "file_path" in locals():
            try:
                os.remove(file_path)
            except OSError:
                pass
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=PDFListResponse)
def list_pdfs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(PDF).count()
    pdfs = db.query(PDF).offset(skip).limit(limit).all()

    return PDFListResponse(items=pdfs, total=total, skip=skip, limit=limit)


@router.get("/{pdf_id}", response_model=PDFResponse)
def get_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return pdf


@router.get("/download/{pdf_id}")
def download_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")

    if not os.path.exists(pdf.path):
        db.delete(pdf)
        db.commit()
        raise HTTPException(status_code=404, detail="PDF file not found on server")

    return FileResponse(pdf.path, filename=pdf.filename, media_type="application/pdf")


@router.delete("/{pdf_id}")
def delete_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")

    try:
        os.remove(pdf.path)
    except OSError as e:
        print(f"Error deleting file: {e}")

    db.delete(pdf)
    db.commit()
    return {"message": "PDF deleted successfully"}
