import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command

from core.db import BotDB
from core.settings import settings

bot_db_instance = BotDB("usersid.db")


async def start_bot():
    await bot.send_message(settings.bots.admin_id, text='Бот начал работу')


async def stop_bot():
    await bot.send_message(settings.bots.admin_id, text='Бот прекратил работу')


default_bot_properties = DefaultBotProperties(parse_mode="HTML")
bot = Bot(token=settings.bots.bot_token, default=default_bot_properties)
dp = Dispatcher()
dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)


@dp.message(Command('subscribe'))
async def send_subcribe(message: types.Message):
    user_id = message.from_user.id
    if not bot_db_instance.user_exists(user_id):
        bot_db_instance.add_user(message.from_user.id)
        await bot.send_message(user_id, "Подписка на рассылку бота оформлена!")
    else:
        await bot.send_message(user_id, "Вы уже подписаны на рассылку бота!")


@dp.message(Command('unsubscribe'))
async def send_unsubcribe(message: types.Message):
    user_id = message.from_user.id
    if bot_db_instance.user_exists(user_id):
        print("delete")
        bot_db_instance.delete_user(message.from_user.id)
        await bot.send_message(user_id, "Подписка на рассылку приостановлена!")
    else:
        await bot.send_message(user_id, "Вы и так не подписаны на рассылку!")


@dp.message(CommandStart())
async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/help"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Используй команду /help"
    )
    await bot.send_message(message.from_user.id,
                           "Привет, это бот, оповещающий об аномальных изменениях цен на акции компаний, для контроля "
                           "подписки на рассылку нажми /help",
                           reply_markup=keyboard)


@dp.message(Command('help'))
async def send_help(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/subscribe"),
            types.KeyboardButton(text="/unsubscribe")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Подпишись или отпишись от рассылки"
    )
    await bot.send_message(message.from_user.id,
                           "Бот мониторит аномалии в акциях и сообщает о них пользователю\n<b>Для подписки на "
                           "рассылку об аномалиях используйте команду:</b>\n\n/subscribe\n\n<b>Для отписки от "
                           "рассылки:</b>\n\n/unsubscribe",
                           reply_markup=keyboard)


async def anomaly_report(anomaly_bot: Bot, newname: str, percent: float):
    user_ids = bot_db_instance.id_for_print()
    print(user_ids)
    for user_id_tuple in user_ids:
        user_id = user_id_tuple[0]
        await anomaly_bot.send_message(chat_id=user_id,
                                       text=f'Акции компании <b>{newname}</b> изменились на <b>{percent:.2f}</b>%!',
                                       parse_mode="HTML")


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        bot_db_instance.close()


if __name__ == '__main__':
    asyncio.run(main())
