from datetime import date
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    category: str = "General"
    due_date: date | None = None
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    category: str | None = None
    due_date: date | None = None
    completed: bool | None = None
class TaskOut(TaskCreate):
    id: int
    completed: bool
    model_config = ConfigDict(from_attributes=True)
class ProgressCreate(BaseModel):
    topic: str = Field(min_length=1, max_length=120)
    solved: int = Field(ge=0)
    total: int = Field(ge=0)
class ProgressOut(ProgressCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
class MaterialCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    url: str = Field(min_length=8, max_length=1000)
    category: str = "General"
class MaterialOut(MaterialCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
