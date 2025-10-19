from src.domain.entities.user import User
from src.domain.exceptions import UserNotFoundError, PhoneBadFormatError, \
    PhoneAlreadyExistsError, PhoneBadCountryError
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

    async def is_user_exists(self, user_id: int) -> bool:
        async with self.__uow.atomic():
            try:
                user = await self.__user_repo.get_user(user_id)
            except UserNotFoundError:
                return False
            except Exception:
                raise
            return True

    async def validate_phone(self, phone_number: str) -> str:
        phone_number = phone_number.strip()
        if phone_number.startswith("+7"):
            phone_number = "8" + phone_number[2:]
        digits = []
        for symbol in phone_number:
            if symbol.isdigit():
                digits.append(symbol)
        phone_number = "".join(digits)
        if len(phone_number) != 11:
            raise PhoneBadFormatError
        if not phone_number.startswith("8"):
            raise PhoneBadCountryError

        async with self.__uow.atomic():
            is_existing = await self.__user_repo.is_phone_number_existing(phone_number)
            if is_existing:
                raise PhoneAlreadyExistsError
        return phone_number
