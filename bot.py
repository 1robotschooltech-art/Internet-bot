from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

API_TOKEN = '8694337840:AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    name = State()
    surname = State()
    address = State()
    phone = State()

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
