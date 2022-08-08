from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class School(BaseModel):
    designation: str
    name: str
    phone: str


class Class(BaseModel):
    teacherId: int
    students: List[int]
    dateAdded: Optional[str]
