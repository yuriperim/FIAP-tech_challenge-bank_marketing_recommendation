from enum import Enum
from pydantic import BaseModel, Field


class Education(str, Enum):
    illiterate = "illiterate"
    basic_4y = "basic.4y"
    basic_6y = "basic.6y"
    basic_9y = "basic.9y"
    high_school = "high.school"
    professional_course = "professional.course"
    university_degree = "university.degree"
    unknown = "unknown"


class Job(str, Enum):
    admin = "admin."
    blue_collar = "blue-collar"
    entrepreneur = "entrepreneur"
    housemaid = "housemaid"
    management = "management"
    retired = "retired"
    self_employed = "self-employed"
    services = "services"
    student = "student"
    technician = "technician"
    unemployed = "unemployed"
    unknown = "unknown"


class MaritalStatus(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    unknown = "unknown"


class YesNoUnknown(str, Enum):
    yes = "yes"
    no = "no"
    unknown = "unknown"


class PreviousOutcome(str, Enum):
    success = "success"
    failure = "failure"
    nonexistent = "nonexistent"


class CustomerRequest(BaseModel):
    age: int = Field(
        ...,
        ge=17,
        le=100,
        description="Idade (anos)"
    )
    education: Education
    job: Job
    marital: MaritalStatus
    default: YesNoUnknown = Field(
        ...,
        description="Tem dívida em atraso (default)?"
    )
    poutcome: PreviousOutcome = Field(
        ...,
        description="Resultado da última campanha"
    )
