from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import string, random

@dataclass
class Url:
    id: Optional[int]
    short_url: str
    long_url: str
    created_at: Optional[datetime] = None


@dataclass
class User:
    username: str
    password: str


class UrlRepository(ABC):
    @abstractmethod
    def save(self, url: Url) -> Url:
        pass

    @abstractmethod
    def find_by_short_url(self, short_url: str) -> Optional[Url]:
        pass

    @abstractmethod
    def find_by_id(self, url_id: int) -> Optional[Url]:
        pass

    @abstractmethod
    def get_all(self) -> List[Url]:
        pass

    @abstractmethod
    def update(self, url_id: int, short_url: str, long_url:str) -> Optional[Url]:
        pass

    @abstractmethod
    def delete(self, url_id: int) -> bool:
        pass

    @abstractmethod
    def exists_by_short_url(self, short_url: str) -> bool:
        pass


class AuthRepository(ABC):
    @abstractmethod
    def validate_user(self, username: str, password: str) -> bool:
        pass