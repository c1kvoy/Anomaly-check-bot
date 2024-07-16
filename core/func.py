import os
import time
import csv
from aiogram import Bot
from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from db import BotDB
from settings import settings
bot_db_instance = BotDB("usersid.db")


default_bot_properties = DefaultBotProperties(parse_mode="HTML")
bot = Bot(token=settings.bots.bot_token, default=default_bot_properties)
dp = Dispatcher()
TOKEN = ""
CSV_FILE_PATH = "Russian_Stocks.csv"

prices_data = {}

def load_figi_list(csv_file_path):
    figi_to_name = {}
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['figi'] and row['Company']:
                figi_to_name[row['figi']] = row['Company']
    return figi_to_name

def request_iterator(figi_list):
    yield MarketDataRequest(
        subscribe_candles_request=SubscribeCandlesRequest(
            waiting_close=True,
            subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
            instruments=[
                CandleInstrument(
                    figi=figi,
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIVE_MINUTES,
                )
                for figi in figi_list
            ],
        )
    )
    while True:
        time.sleep(1)

async def process_candle_data(candle, figi_to_name):
    figi = candle.figi
    company_name = figi_to_name.get(figi, "Неизвестная компания")
    open_price = candle.open.units + candle.open.nano / 1e9
    close_price = candle.close.units + candle.close.nano / 1e9
    change_percent = ((close_price - open_price) / open_price) * 100
    if abs(change_percent) > 0.4:
        print(f"Акции компании {company_name} изменились на {change_percent:.3f} %")
        info = f"Акции компании <b>{company_name}</b> изменились на <b>{change_percent:.3f}</b> %"
        user_ids = bot_db_instance.id_for_print()
        for user in user_ids:
            try:
                await send_message(user, info)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user}: {e}")
                continue


async def send_message(user_id, message):
        await bot.send_message(user_id, message)
        print(message)


async def main():
    try:
        dp.start_polling(bot)
        print('bot')
        figi_to_name = load_figi_list(CSV_FILE_PATH)
        figi_list = list(figi_to_name.keys())
        with Client(TOKEN) as client:
            print('client')
            for marketdata in client.market_data_stream.market_data_stream(
                    request_iterator(figi_list)
            ):
                if marketdata.candle:
                    print('cli')
                    await process_candle_data(marketdata.candle, figi_to_name)
                else:
                    print("Получены данные без свечи: ", marketdata)
    finally:
        await bot.session.close()
        bot_db_instance.close()

if __name__ == "__main__":
    asyncio.run(main())
