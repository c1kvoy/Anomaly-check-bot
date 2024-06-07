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

def grafic(data, name):
    pyplot.plot(data)
    plt.title('График изменения цены акции', fontsize=20)
    plt.xlabel('время')
    plt.ylabel('цена')
    plt.text(0.3, 3, name, fontsize=16, bbox={'facecolor':'blue', 'alpha':0.2})
    pyplot.show()

async def main():
    bot = Bot(token=settings.bots.bot_token)
    condition, percent, newname = calculate_percent(data, name)
    if condition:
        await anomaly_report(bot, newname, percent)

if __name__ == '__main__':
    asyncio.run(main())