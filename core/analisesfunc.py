import asyncio
from main import anomaly_report
from aiogram import Bot
from core.settings import settings

data = {"Gazprom": [1.2, 200.2], "Huypizda": [2000, 112]}

async def calculate_percent(name, values):
    condition = False
    prev_price = values[0]
    now_price = values[1]
    change_percent = ((now_price - prev_price) / prev_price) * 100
    if abs(change_percent) > 1:
        condition = True
    return condition, change_percent, name

async def main():
    bot = Bot(token=settings.bots.bot_token)
    for name, values in data.items():
        condition, percent, newname = await calculate_percent(name, values)
        if condition:
            await anomaly_report(bot, newname, percent)

if __name__ == '__main__':
    asyncio.run(main())