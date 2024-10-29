from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PDFBase(BaseModel):
    filename: str


class PDFResponse(PDFBase):
    id: int
    path: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnnotationBase(BaseModel):
    page: int
    x: int
    y: int
    width: int
    height: int
    content: str


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationResponse(AnnotationBase):
    id: int
    pdf_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    pdf_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PDFListResponse(BaseModel):
    items: List[PDFResponse]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)


# TODO: note and annotation schemas , further testing
