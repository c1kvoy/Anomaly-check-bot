from aiogram import types

async def get_start(message: types.Message):
    await message.answer (f'Привет {message. from_user. first_name}. Рад тебя видеть!')




