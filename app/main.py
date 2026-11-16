from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routers.tasks import router as task_router
from app.routers.users import router as user_router
from app.routers.projects import router as project_router
from app.rate_limit import limiter

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
def root():
    return {"message": "TaskForge API is running"}


app.include_router(task_router, prefix="/tasks")
app.include_router(user_router, prefix="/users")
app.include_router(project_router, prefix="/projects")