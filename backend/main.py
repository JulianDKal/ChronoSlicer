from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import api_pdf_upload, api_pdf_extraction
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize services, database connections
    print("Starting up...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down...")

app = FastAPI(
    title="Your API",
    description="API for Vue + Three.js app",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_pdf_upload.router, prefix="/api")
app.include_router(api_pdf_extraction.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

# API Routes
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/lines")
async def get_lines():
    zigzag_lines = [
        {"x1": -6, "y1": 4, "x2": -4, "y2": 2},
        {"x1": -4, "y1": 2, "x2": -2, "y2": 4},
        {"x1": -2, "y1": 4, "x2": 0, "y2": 2},
        {"x1": 0, "y1": 2, "x2": 2, "y2": 4},
        {"x1": 2, "y1": 4, "x2": 4, "y2": 2},
        {"x1": 4, "y1": 2, "x2": 6, "y2": 4},
    ]

    return {
        "lines": zigzag_lines
    }