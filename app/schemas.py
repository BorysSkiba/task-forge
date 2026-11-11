from pydantic import BaseModel, EmailStr


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    project_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    project_id: int | None = None


class TaskResponse(TaskCreate):
    id: int
    title: str
    description: str | None
    completed: bool
    project_id: int | None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    user_id: int