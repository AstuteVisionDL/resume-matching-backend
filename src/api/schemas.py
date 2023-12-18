"""Schemas for requests and responses"""
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class HealthCheckResponse(BaseModel):
    """
    Response scheme for checking the health of the service
    """

    status: str = "ok"


class ErrorMessage(BaseModel):
    """
    Error response scheme
    """

    message: str


class SalaryType(str, Enum):
    no = "no"
    value = "value"
    range = "range"


class MoveType(str, Enum):
    no = "No"
    may_be = "May be"
    yes = "Yes"


class EmploymentType(str, Enum):
    full_time = "Full-time"
    part_time = "Part-time"
    project = "Project"
    volunteering = "Volunteering"
    internship = "Internship"


class ScheduleType(str, Enum):
    full = "Full"
    small_shift = "Small shift"
    flexible = "Flexible"
    remote = "Remote"
    large_shift = "Large shift"


class EducationType(str, Enum):
    middle = "Middle"
    middle_special = "Middle special"
    almost_high = "Almost high"
    high = "High"


class Vacancy(BaseModel):
    name: str
    salary_type: SalaryType
    min_value: Optional[float]
    max_value: Optional[float]
    value: Optional[float]
    city: str
    move: MoveType
    employment: list[EmploymentType]
    schedule: list[ScheduleType]
    education: EducationType


class Resume(BaseModel):
    name: str
    salary_type: SalaryType
    min_value: Optional[float]
    max_value: Optional[float]
    value: Optional[float]
    city: str
    move: MoveType
    schedule: list[ScheduleType]
    education: EducationType
    employment: list[EmploymentType]


class MatchingRequest(BaseModel):
    vacancy: Vacancy
    resume: Resume


class MatchingResponse(BaseModel):
    value: float
    message: str
