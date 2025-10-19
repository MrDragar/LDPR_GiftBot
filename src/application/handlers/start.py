import logging

from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from src.application.keyboards.personal_data_keyboard import \
    get_personal_data_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
start_command_router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message()
@start_command_router.message(filters.CommandStart())
async def start(message: types.Message, user_service: IUserService, state: FSMContext):
    if await user_service.is_user_exists(message.from_user.id):
        logging.debug(f"User {message.from_user.id} already exists")
        return await message.reply("Вы уже успешно зарегистрировались")

    logging.debug(f"User {message.from_user.id} Start conversation")
    await message.reply(
        "Здравствуйте! ЛДПР дарит вашему ребёнку новогоднее чудо! \n\n"
        "Чтобы мы могли передать подарок, пожалуйста, укажите Ваши имя и номер "
        "телефона для связи. Так мы сможем делиться с Вами полезными и тёплыми "
        "материалами для всей семьи: открытки к праздникам, раскраски с "
        "весёлыми персонажами, журналы полезных привычек и многое другое. "
        "Это и не только станет приятным дополнением к нашему общению!"
    )

    await message.reply("Для начала дайте согласие на обработку персональных данных", reply_markup=get_personal_data_keyboard())
    await state.set_state(RegistrationStates.personal_data)
