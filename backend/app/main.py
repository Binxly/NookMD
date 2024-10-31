import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base

from app.routers import pdf


# Define allowed origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add production URLs when deploying
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create uploads directory
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Type"],
)

app.include_router(pdf.router)


@app.get("/")
async def root():
    return {"message": "Welcome to NookMD API"}
