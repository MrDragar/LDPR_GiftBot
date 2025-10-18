from abc import ABC, abstractmethod

from src.domain.entities.user import User


class IUserService(ABC):
    @abstractmethod
    async def create_user(
            self, user_id: int, username: str | None,
            fio: str, phone_number: str
    ) -> User:
        ...

