from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = '8694337840:AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g'  # ← вставь реальный токен от BotFather

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()
    surname = State()
    address = State()
    phone = State()
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await Form.name.set()
    await message.reply("Привет! Введи своё имя.")

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.surname.set()  # ← next() лучше заменить на явный set
    await message.reply("Теперь фамилию.")

@dp.message_handler(state=Form.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await Form.address.set()
    await message.reply("Адрес.")

@dp.message_handler(state=Form.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await Form.phone.set()
    await message.reply("Телефон.")

@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # ← тут была ошибка: send_message без скобок и без запятой
    await bot.send_message(
        chat_id=8240806734,  # ← твой ID, надеюсь правильный
        text=f"Клиент:\n"
             f"Имя: {data.get('name', 'не указано')}\n"
             f"Фамилия: {data.get('surname', 'не указано')}\n"
             f"Адрес: {data.get('address', 'не указано')}\n"
             f"Тел: {message.text}"
    )
    await message.reply("Готово! Свяжемся.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
