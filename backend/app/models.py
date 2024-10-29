from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    path = Column(String)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(UTC))

    annotations = relationship("Annotation", back_populates="pdf")
    notes = relationship("Note", back_populates="pdf")


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey("pdfs.id"))
    page = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    pdf = relationship("PDF", back_populates="annotations")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey("pdfs.id"))
    content = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    pdf = relationship("PDF", back_populates="notes")
