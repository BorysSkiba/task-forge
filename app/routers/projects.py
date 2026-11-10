from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project as ProjectModel
from app.schemas import ProjectCreate, ProjectResponse
from app.security import get_current_user_id

router = APIRouter(tags=["projects"])


@router.post("", status_code=201)
def create_project(project: ProjectCreate, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    new_project = ProjectModel(
        name=project.name,
        description=project.description,
        user_id=int(user_id)
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project
