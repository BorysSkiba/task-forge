from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.routers.tasks import router as task_router
from app.routers.users import router as user_router
from app.routers.projects import router as project_router
from app.rate_limit import limiter
from app.config import settings


def create_app() -> FastAPI:
    application = FastAPI(
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        openapi_url="/openapi.json" if settings.enable_docs else None,
    )

    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts,
    )

    application.include_router(task_router, prefix="/tasks")
    application.include_router(user_router, prefix="/users")
    application.include_router(project_router, prefix="/projects")

    @application.get("/")
    def root():
        return {"message": "TaskForge API is running"}

    return application


app = create_app()
