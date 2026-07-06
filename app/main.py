from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# Import models so Base knows about them before create_all
from app.models import user, student, course, grade  # noqa: F401

from app.api.routers import auth, users, students, courses, grades, analytics, ml, tutor

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dev-only: auto-create tables. In production, use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(students.router, prefix=settings.API_V1_PREFIX)
app.include_router(courses.router, prefix=settings.API_V1_PREFIX)
app.include_router(grades.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)
app.include_router(ml.router, prefix=settings.API_V1_PREFIX)
app.include_router(tutor.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": "Student Performance Tracker API is running"}
