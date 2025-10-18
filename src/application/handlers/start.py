from aiogram import Router, types

from src.application.keyboards.personal_data_keyboard import \
    get_personal_data_keyboard
from src.services.interfaces import IUserService

router = Router(name=__name__)


@router.message()
async def start(message: types.Message, user_service: IUserService):
    if user_service is None:
        return await message.reply("Вы уже успешно зарегистрировались")
    await message.reply(
        "Здравствуйте! ЛДПР дарит вашему ребенку новогоднее чудо!"
        " Чтобы получить подарок, пожалуйста, введите ваше имя и номер телефона для подтверждения. "
        "Продолжая, вы соглашаетесь на получение актуальных новостей от партии"
    )
    await message.reply("Для начала примите согласие на обработку персональных данных", reply_markup=get_personal_data_keyboard())
