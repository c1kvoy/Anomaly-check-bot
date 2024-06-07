from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.db import BotDB
from core.settings import settings

bot_db_instance = BotDB("../../../../Documents/database/usersid.db")


async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/help"),
            types.KeyboardButton(text="/report")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Используй команду /help или /оценка"
    )
    await message.answer(
        "Привет, это бот, оповещающий об аномальных изменениях цен на акции компаний, для контроля "
        "подписки на рассылку нажми /help",
        reply_markup=keyboard
    )


async def send_help(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/subscribe"),
            types.KeyboardButton(text="/unsubscribe"),
            types.KeyboardButton(text="/report")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Подпишись или отпишись от рассылки"
    )
    await message.answer(
        "Бот мониторит аномалии в акциях и сообщает о них пользователю\n<b>Для подписки на "
        "рассылку об аномалиях используйте команду:</b>\n\n/subscribe\n\n<b>Для отписки от "
        "рассылки:</b>\n\n/unsubscribe\n\n<b>Для оценки работы бота:</b>\n\n /report",
        reply_markup=keyboard
    )


async def send_subscribe(message: types.Message):
    user_id = message.from_user.id
    if not bot_db_instance.user_exists(user_id):
        bot_db_instance.add_user(user_id)
        await message.answer("Подписка на рассылку бота оформлена!")
    else:
        await message.answer("Вы уже подписаны на рассылку бота!")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="1", callback_data="1"))
    builder.add(types.InlineKeyboardButton(text="2", callback_data="2"))
    builder.add(types.InlineKeyboardButton(text="3", callback_data="3"))
    builder.add(types.InlineKeyboardButton(text="4", callback_data="4"))
    builder.add(types.InlineKeyboardButton(text="5", callback_data="5"))
    await message.answer(
        "Оцените действия разработчика!",
        reply_markup=builder.as_markup()
    )


async def send_report(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="1", callback_data="1"))
    builder.add(types.InlineKeyboardButton(text="2", callback_data="2"))
    builder.add(types.InlineKeyboardButton(text="3", callback_data="3"))
    builder.add(types.InlineKeyboardButton(text="4", callback_data="4"))
    builder.add(types.InlineKeyboardButton(text="5", callback_data="5"))
    await message.answer(
        "Оцените действия разработчика!",
        reply_markup=builder.as_markup()
    )


async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.bot.answer_callback_query(callback_query.id)
    await callback_query.bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"<b>Спасибо за оценку действий бота</b>"
    )
    await callback_query.bot.send_message(
        chat_id=settings.bots.admin_id,
        text=f'Пользователь <b>@{callback_query.from_user.username}</b> поставил оценку <b>{callback_query.data}</b> '
             f'работе бота '
    )


async def send_unsubscribe(message: types.Message):
    user_id = message.from_user.id
    if bot_db_instance.user_exists(user_id):
        print("delete")
        bot_db_instance.delete_user(message.from_user.id)
        await message.answer("Подписка на рассылку приостановлена!")
    else:
        await message.answer("Вы и так не подписаны на рассылку!")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="1", callback_data="1"))
    builder.add(types.InlineKeyboardButton(text="2", callback_data="2"))
    builder.add(types.InlineKeyboardButton(text="3", callback_data="3"))
    builder.add(types.InlineKeyboardButton(text="4", callback_data="4"))
    builder.add(types.InlineKeyboardButton(text="5", callback_data="5"))
    await message.answer(
        "Оцените действия разработчика!",
        reply_markup=builder.as_markup()
    )
