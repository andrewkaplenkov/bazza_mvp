from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    city: str
    address: Optional[str] = None
    description: Optional[str] = None
    completion_date: Optional[str] = None
    price_from: Optional[float] = None
    image_url: Optional[str] = None
    reward_percent: Optional[float] = 2.1
    is_active: Optional[bool] = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    completion_date: Optional[str] = None
    price_from: Optional[float] = None
    image_url: Optional[str] = None
    reward_percent: Optional[float] = None
    is_active: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class KnowledgeBaseBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    project_id: Optional[int] = None


class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass


class KnowledgeBaseUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    project_id: Optional[int] = None


class KnowledgeBaseResponse(KnowledgeBaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PartnerRewardBase(BaseModel):
    project_id: int
    reward_percent: float
    description: Optional[str] = None


class PartnerRewardCreate(PartnerRewardBase):
    pass


class PartnerRewardUpdate(BaseModel):
    project_id: Optional[int] = None
    reward_percent: Optional[float] = None
    description: Optional[str] = None


class PartnerRewardResponse(PartnerRewardBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True