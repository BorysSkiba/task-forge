from fastapi import FastAPI

from app.routers.tasks import router as task_router
from app.routers.users import router as user_router
from app.routers.projects import router as project_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "TaskForge API is running"}


app.include_router(task_router, prefix="/tasks")
app.include_router(user_router, prefix="/users")
app.include_router(project_router, prefix="/projects")