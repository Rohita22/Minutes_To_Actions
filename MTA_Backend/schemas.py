
from pydantic import BaseModel #instead of manual structuring of json, this can automatically check if data received is of crt data type
from typing import List, Optional #optional is to make a field optional


class SessionCreate(BaseModel):
    title: Optional[str] = None
    notes: str


class ActionItem(BaseModel):
    owner: str
    task: str
    due_date: Optional[str] = None
    priority: Optional[str] = None #ENUM : High, medium, low


class SessionResponse(BaseModel):
    session_id: int
    title: str #if user doesn't enter a title show as untitled meeting
    created_at: str
    summary: List[str]
    decisions: List[str]
    action_items: List[ActionItem]
