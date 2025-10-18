from src.core.di import DeclarativeContainer, providers
from src.domain.interfaces import IUnitOfWork, IUserRepository

from src.infrastructure import Database, UnitOfWork
from src.infrastructure.repositories import UserRepository
from src.infrastructure.interfaces import IDatabase

from src.services import UserService
from src.services.interfaces import IUserService


class Container(DeclarativeContainer):
    database: providers.Singleton[IDatabase] = providers.Singleton(
        Database, "db.sqlite3"
    )
    uow: providers.Singleton[IUnitOfWork] = providers.Singleton(
        UnitOfWork, database=database
    )
    user_repository: providers.Factory[IUserRepository] = providers.Factory(
        UserRepository, uow=uow
    )
    user_service: providers.Factory[IUserService] = providers.Factory(
        UserService, user_repo=user_repository, uow=uow
    )
