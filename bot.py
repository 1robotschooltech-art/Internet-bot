from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = 'ТВОЙ_ТОКЕН'  # вставь от BotFather

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()
    surname = State()
    address = State()
    phone = State()

@dp.message_handler(commands= )
async def start(message: types.Message):
    await Form.name.set()
    await message.reply("Привет! Введи своё имя.")

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.next()
    await message.reply("Фамилию.")

@dp.message_handler(state=Form.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await Form.next()
    await message.reply("Адрес.")

@dp.message_handler(state=Form.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await Form.next()
    await message.reply("Телефон.")

@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message 8240806734  
        f"Клиент:\nИмя: {data }\nФамилия: {data }\nАдрес: {data }\nТел: {message.text}")
    await message.reply("Готово! Свяжемся.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
