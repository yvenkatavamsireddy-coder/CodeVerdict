from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ─── User ───────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True

# ─── Problem ────────────────────────────────────

class ProblemCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    time_limit: int = 5
    memory_limit: int = 128

class ProblemResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    time_limit: int
    memory_limit: int

    class Config:
        from_attributes = True

# ─── TestCase ───────────────────────────────────

class TestCaseCreate(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False

# ─── Submission ─────────────────────────────────

class SubmissionCreate(BaseModel):
    problem_id: int
    code: str

class SubmissionResponse(BaseModel):
    id: int
    problem_id: int
    verdict: str
    runtime: Optional[int]
    submitted_at: datetime

    class Config:
        from_attributes = True