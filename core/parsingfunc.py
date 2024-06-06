import asyncio
from main import anomaly_report
from aiogram import Bot
from core.settings import settings

data = [14,20]
name = 'Gazprom'
def calculate_percent(data, name):
    condition = False
    prev_price = data[0]
    now_price = data[1]
    change_percent = ((now_price - prev_price) / prev_price) * 100
    if abs(change_percent) > 1:
        condition = True
    return condition, change_percent, name

async def main():
    bot = Bot(token=settings.bots.bot_token)
    condition, percent, newname = calculate_percent(data, name)
    if condition:
        await anomaly_report(bot, newname, percent)

if __name__ == '__main__':
    asyncio.run(main())