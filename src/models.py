from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id")
    activity: Optional["Activity"] = Relationship(back_populates="participants")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = ""
    schedule: Optional[str] = None
    max_participants: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    participants: List[Participant] = Relationship(back_populates="activity")
