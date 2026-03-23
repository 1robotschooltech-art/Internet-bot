import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import speedtest  # pip install speedtest-cli

bot = Bot(token="AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g")
dp = Dispatcher(storage=MemoryStorage())

# Клавиатура меню
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
menu_kb.add(
    KeyboardButton("Проверить скорость"),
    KeyboardButton("Сообщить о сбое"),
    KeyboardButton("Мой баланс"),
    KeyboardButton("Поддержка")
)

class Form(StatesGroup):
    outage_address = State()
    outage_type = State()
    support_message = State()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот твоего провайдера. Выбери, что нужно:",
        reply_markup=menu_kb
    )

@dp.message(lambda m: m.text == "Проверить скорость")
async def speed_test(message: types.Message):
    await message.answer("Запускаю тест... подожди 10 секунд.")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # в Мбит/с
        upload = st.upload() / 1_000_000
        await message.answer(
            f"Скорость: скачивание — {download:.2f} Мбит/с\n"
            f"загрузка — {upload:.2f} Мбит/с\n"
            f"пинг — {st.results.ping} мс"
        )
    except Exception:
        await message.answer("Не смог измерить. Проверь интернет или попробуй позже.")

@dp.message(lambda m: m.text == "Сообщить о сбое")
async def outage_start(message: types.Message, state: FSMContext):
    await message.answer("Напиши адрес, где нет интернета (улица, дом, квартира):")
    await state.set_state(Form.outage_address)

@dp.message(Form.outage_address)
async def outage_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Что случилось? (например: 'нет связи', 'медленно', 'постоянно рвётся')")
    await state.set_state(Form.outage_type)

@dp.message(Form.outage_type)
async def outage_type(message: types.Message, state: FSMContext):
    data = await state.get_data()
    address = data.get("address")
    problem = message.text
    # Тут можно отправить в твою систему тикетов, например print или в базу
    await message.answer(
        f"Сбой зафиксирован!\nАдрес: {address}\nПроблема: {problem}\n"
        "Техник свяжется в течение часа. Спасибо."
    )
    await state.clear()

@dp.message(lambda m: m.text == "Мой баланс")
async def balance(message: types.Message):
    # Здесь подключи свою базу данных или API
    await message.answer("Баланс: 45.67 USD (на 23 марта 2026). Всё ок!")

@dp.message(lambda m: m.text == "Поддержка")
async def support_start(message: types.Message, state: FSMContext):
    await message.answer("Напиши свой вопрос или проблему:")
    await state.set_state(Form.support_message)

@dp.message(Form.support_message)
async def support_send(message: types.Message, state: FSMContext):
    await message.answer("Спасибо! Твой запрос передан в поддержку. Ответят в течение 15 минут.")
    # Тут реально шлёшь в чат поддержки или Zendesk
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
