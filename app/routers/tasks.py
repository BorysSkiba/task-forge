from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Literal, List, Annotated

from app.database import get_db
from app.models import Task as TaskModel
from app.models import Project as ProjectModel
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.security import get_current_user_id

router = APIRouter(tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def get_tasks(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user_id),
        completed: bool | None = None,
        project_id: int | None = None,
        sort_by: str | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0
):
    filters = [
        TaskModel.user_id == user_id,
    ]

    allowed_sort_fields = {
        "id": TaskModel.id,
        "title": TaskModel.title,
        "completed": TaskModel.completed,
        "project_id": TaskModel.project_id,
    }

    if completed is not None:
        filters.append(TaskModel.completed == completed)

    if project_id is not None:
        filters.append(TaskModel.project_id == project_id)

    statement = select(TaskModel).where(*filters)

    if sort_by is not None:
        if sort_by not in allowed_sort_fields:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        sort_column = allowed_sort_fields[sort_by]

        if sort_order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())

        statement = statement.offset(offset).limit(limit)

    tasks = db.scalars(statement).all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    statement = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    if task.project_id is not None:
        statement = select(ProjectModel).where(ProjectModel.id == task.project_id, ProjectModel.user_id == user_id)
        project = db.scalars(statement).first()

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        new_task.project_id = task.project_id

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    statement = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": f"Task {task_id} deleted"}


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    statement = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
    task = db.scalars(statement).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)

    if "project_id" in update_data:
        project_id = update_data["project_id"]

        if project_id is not None:
            statement = select(ProjectModel).where(
                ProjectModel.id == project_id,
                ProjectModel.user_id == user_id
            )

            project = db.scalars(statement).first()

            if project is None:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found"
                )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task