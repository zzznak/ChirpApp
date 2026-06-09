from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    timestamp: Optional[datetime] = None
    is_encrypted: bool = True
    is_read: bool = False
    id: Optional[int] = None

@dataclass
class User:
    username: str
    email: str
    avatar: str
    status: str = "Привет!"
    is_online: bool = False
    public_key: Optional[str] = None

@dataclass
class Chat:
    name: str
    last_message: str
    timestamp: str
    avatar: str
    unread_count: int = 0
    is_online: bool = False

@dataclass
class Group:
    id: int
    name: str
    avatar: str
    members_count: int
    created_at: datetime
