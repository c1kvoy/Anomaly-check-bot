import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command

from handlers import start, send_help, send_subscribe, send_report, process_callback, send_unsubscribe
from core.db import BotDB
from core.settings import settings

bot_db_instance = BotDB("../../../../Documents/database/usersid.db")


async def start_bot():
    await bot.send_message(settings.bots.admin_id, text='Бот начал работу')


async def stop_bot():
    await bot.send_message(settings.bots.admin_id, text='Бот прекратил работу')


default_bot_properties = DefaultBotProperties(parse_mode="HTML")
bot = Bot(token=settings.bots.bot_token, default=default_bot_properties)
dp = Dispatcher()
dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)


# Регистрация хендлеров
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await start(message)


@dp.message(Command('help'))
async def help_handler(message: types.Message):
    await send_help(message)


@dp.message(Command('subscribe'))
async def subscribe_handler(message: types.Message):
    await send_subscribe(message)


@dp.message(Command('report'))
async def report_handler(message: types.Message):
    await send_report(message)


@dp.callback_query(lambda c: c.data in ['1', '2', '3', '4', '5'])
async def callback_handler(callback_query: types.CallbackQuery):
    await process_callback(callback_query)


@dp.message(Command('unsubscribe'))
async def unsubscribe_handler(message: types.Message):
    await send_unsubscribe(message)


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
