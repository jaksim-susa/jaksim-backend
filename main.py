from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi import FastAPI

from app.api import analysis, auth, goal, record
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # 서버 시작 시 DB 초기화
    yield

app = FastAPI(
    title="JAKSHIM API",
    description="JAKSHIM Backend API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://jakshim-frontend-one.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(goal.router, prefix="/api/goals", tags=["goals"])
app.include_router(record.router, prefix="/api/records", tags=["records"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}