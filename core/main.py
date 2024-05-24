import asyncio
from aiogram import Bot, Dispatcher
from core.handlers.basic import get_start
from core.settings import settings
import logging

async def anomaly_report(bot: Bot, newname: str, percent: float):
    await bot.send_message(chat_id='-1002226165629', text=f'Акции компании {newname} изменились на {percent}%!')

async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот начал работу')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот прекратил работу')

async def start():
    global report_sent
    report_sent = False  # Сброс переменной при каждом запуске
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - [%(name)s]"
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=settings.bots.bot_token)
    dp = Dispatcher()
    dp.message.register(get_start)
    dp.message.register(anomaly_report)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())