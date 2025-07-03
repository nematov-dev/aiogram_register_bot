import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from decouple import config

from database import create_users_table,add_user,check_id

# Token
API_TOKEN = config("API_TOKEN")

# Log
logging.basicConfig(level=logging.DEBUG)

# Bot va dispatcher yaratamiz
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# FSM holatlari
class UserForm(StatesGroup):
    name = State()
    surname = State()
    number = State()

# /start komandasi
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not check_id(telegram_id):
        await message.answer("Ismingizni kiriting:")
        await state.set_state(UserForm.name)
    else:
        await message.answer("Siz oldin ro'yxatdan o'tgansiz!")

# Ismni qabul qilish
@dp.message(UserForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(UserForm.surname)

# Familiyani qabul qilish
@dp.message(UserForm.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Telefon raqam kiriting:")
    await state.set_state(UserForm.number)

# Telefon nomer qabul qilish
@dp.message(UserForm.number)
async def process_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(UserForm.number)
    data = await state.get_data()
    telegram_id = message.from_user.id
    username = message.from_user.username
    result = add_user(telegram_id=telegram_id,name=data['name'],surname=data['surname'],phone=data['number'],username=username)
    if result:
        await message.answer(f"Ro'yxatdan muaffaqiyatli o'tdingiz!\nIsm: {data['name']}\nFamiliya: {data['surname']}\nRaqam: {data['number']}")
        await state.clear()  # FSM-ni tozalash
    else:
        await message.answer(f"Ro'yxatdan o'tishda xatolik yuzaga keldi!")

# Bot polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    create_users_table()
    asyncio.run(main())
    