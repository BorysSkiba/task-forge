from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = False
    project_id: int | None = Field(default=None, gt=0)

    @field_validator('title', mode="before")
    @classmethod
    def validate_title(cls, value: str):
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Title cannot be empty")

        return cleaned

    @field_validator('description', mode="before")
    @classmethod
    def validate_description(cls, value: str | None):
        if value is None:
            return None

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Description cannot be empty")

        return cleaned


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = None
    project_id: int | None = Field(default=None, gt=0)

    @field_validator('title', mode="before")
    @classmethod
    def validate_title(cls, value: str | None):
        if value is None:
            raise ValueError("Title cannot be empty")

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Title cannot be empty")

        return cleaned

    @field_validator('description', mode="before")
    @classmethod
    def validate_description(cls, value: str | None):
        if value is None:
            return None

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Description cannot be empty")

        return cleaned


class TaskResponse(TaskCreate):
    id: int
    title: str
    description: str | None
    completed: bool
    project_id: int | None


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator('username', mode="before")
    @classmethod
    def validate_username(cls, value: str):
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Username cannot be empty")

        return cleaned


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator('name', mode="before")
    @classmethod
    def validate_name(cls, value: str):
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Name cannot be empty")

        return cleaned


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator('name', mode="before")
    @classmethod
    def validate_name(cls, value: str | None):
        if value is None:
            raise ValueError("Name cannot be null")

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Name cannot be empty")

        return cleaned


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    user_id: int