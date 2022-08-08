from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class School(BaseModel):
    id: int
    designation: str
    name: str
    phone: str


class Class(BaseModel):
    id: int
    teacherId: int
    students: List[int]
    dateAdded: Optional[str]
