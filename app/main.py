from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import course, q, questions, login,module 
import os

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

origins = os.getenv("ALLOWED_ORIGINS", "")
allow_origins = origins.split(",") if origins else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(course.router)
app.include_router(questions.router)
app.include_router(q.router)
app.include_router(login.router)
app.include_router(module.router)