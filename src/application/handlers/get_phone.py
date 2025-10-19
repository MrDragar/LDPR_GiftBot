import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates
from src.domain import exceptions
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.phone)
async def get_phone_number(message: types.Message, state: FSMContext, user_service: IUserService):
    phone = message.text
    logger.debug(f"Got phone number {phone}")
    try:
        phone = await user_service.validate_phone(phone)
    except exceptions.PhoneBadFormatError:
        return message.reply("Некорректный формат телефона. Введите номер телефона в следующем формате: +79876543210")
    except exceptions.PhoneBadCountryError:
        return message.reply("К сожалению, мы поддерживаем работу только с российскими номерами. Попробуйте ввести другой номер телефона")
    except exceptions.PhoneAlreadyExistsError:
        return message.reply("Пользователь с данным номером телефона уже существует")

    data = await state.get_data()
    fio = data['fio']

    await user_service.create_user(message.from_user.id, message.from_user.username, fio, phone)
    await state.clear()
    await message.reply("Поздравляем, вы успешно зарегистрированы. Переходите по ссылке https://ссылка.пример для получения подарка")
