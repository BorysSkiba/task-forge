from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project as ProjectModel
from app.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.security import get_current_user_id

router = APIRouter(tags=["projects"])


@router.get("")
def get_projects(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    statement = select(ProjectModel).where(ProjectModel.user_id == user_id)

    projects = db.scalars(statement).all()

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    statement = select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)
    project = db.scalars(statement).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.post("", status_code=201, response_model=ProjectResponse)
def create_project(project: ProjectCreate, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    new_project = ProjectModel(
        name=project.name,
        description=project.description,
        user_id=user_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    statement = select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)
    project = db.scalars(statement).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": f"Project {project_id} deleted"}


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    statement = select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)
    project = db.scalars(statement).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project