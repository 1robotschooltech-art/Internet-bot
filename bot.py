from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import asyncio
import os

# Лучше через .env, но пока так
API_TOKEN = '8694337840:AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g'
ADMIN_ID = 8240806734

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    name = State()
    surname = State()
    address = State()
    phone = State()
    email = State()

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.reply("Привет! Введи своё имя.")

@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.surname)
    await message.reply("Фамилию.")

@dp.message(Form.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Form.address)
    await message.reply("Адрес.")

@dp.message(Form.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Form.phone)
    await message.reply("Телефон.")

@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Form.email)
    await message.reply("Теперь email, пожалуйста.")

@dp.message(Form.email)
async def process_email(message: types.Message, state: FSMContext):
    data = await state.get_data()
    email = message.text
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Клиент:\n"
             f"Имя: {data.get('name', '—')}\n"
             f"Фамилия: {data.get('surname', '—')}\n"
             f"Адрес: {data.get('address', '—')}\n"
             f"Тел: {data.get('phone', '—')}\n"
             f"Email: {email}"
    )
    await message.reply("Всё, готово! Скоро свяжемся.")
    await state.finish()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
