from src.domain.entities.user import User
from src.domain.interfaces import IUnitOfWork, IUserRepository
from src.services.interfaces import IUserService


class UserService(IUserService):
    __user_repo: IUserRepository
    __uow: IUnitOfWork

    def __init__(self, user_repo: IUserRepository, uow: IUnitOfWork):
        self.__user_repo = user_repo
        self.__uow = uow

    async def create_user(
            self, user_id: int, username: str | None,
            fio: str, phone_number: str
    ) -> User:
        user = User(
            id=user_id, username=username, phone_number=phone_number, fio=fio
        )
        async with self.__uow.atomic():
            await self.__user_repo.create_user(user)
        return user

