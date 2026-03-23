from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import asyncio

API_TOKEN = '8694337840:AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    name = State()
    surname = State()
    address = State()
    phone = State()
@dp.message(Command("start", "menu"))
async def show_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Самоанализ 10 шагов", callback_data="analiz10")],
        [types.InlineKeyboardButton(text="10 шагов mini", callback_data="mini")],
        [types.InlineKeyboardButton(text="1 шаг на день", callback_data="day1")],
        [types.InlineKeyboardButton(text="Настройки", callback_data="settings")]
    ])
    await message.reply("Выбери, что хочешь:", reply_markup=keyboard)

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
    data = await state.get_data()
    await bot.send_message(
        chat_id=8240806734,
        text=f"Клиент:\nИмя: {data.get('name', 'не указано')}\n"
             f"Фамилия: {data.get('surname', 'не указано')}\n"
             f"Адрес: {data.get('address', 'не указано')}\n"
             f"Тел: {message.text}"
    )
    await message.reply("Готово! Свяжемся.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
