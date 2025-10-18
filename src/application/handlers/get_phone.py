import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.fio)
async def get_phone_number(message: types.Message, state: FSMContext, user_service: IUserService):
    phone = message.text
    logger.debug(f"Got phone number {phone}")
    data = await state.get_data()
    fio = data['fio']

    await user_service.create_user(message.from_user.id, message.from_user.usernamem, fio, phone)
    await state.clear()
    await message.reply("Поздравляем, вы успешно зарегистрированы. Переходите по ссылке https://депутатлдпр.рф для получения подарка")
