import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import speedtest  # pip install speedtest-cli

bot = Bot(token="8694337840:AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g")
dp = Dispatcher(storage=MemoryStorage())

ADMIN_ID = 8240806734

# Глобальный словарь: user_id → данные
user_data ={user_id: {...}}

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Проверить скорость"),
            KeyboardButton(text="Сообщить о сбое")
        ],
        [
            KeyboardButton(text="Мой баланс"),
            KeyboardButton(text="Поддержка")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери, что нужно..."
)

class Registration(StatesGroup):
    name = State()
    surname = State()
    address = State()
    phone = State()
    email = State()

class Form(StatesGroup):
    outage_address = State()
    outage_type = State()
    support_message = State()

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Сначала зарегистрируемся — нужно для твоего аккаунта.")
    await message.answer("Как тебя зовут? (имя)")
    await state.set_state(Registration.name)

@dp.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Фамилия?")
    await state.set_state(Registration.surname)

@dp.message(Registration.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Адрес (улица, дом, квартира):")
    await state.set_state(Registration.address)

@dp.message(Registration.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Номер телефона:")
    await state.set_state(Registration.phone)

@dp.message(Registration.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Email:")
    await state.set_state(Registration.email)

@dp.message(Registration.email)
async def process_email(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "")
    surname = data.get("surname", "")
    address = data.get("address", "")
    phone = data.get("phone", "")
    email = message.text

    user_id = message.from_user.id

    # Сохраняем в глобальный словарь
    user_data = {
        'name': name,
        'surname': surname,
        'address': address,
        'phone': phone,
        'email': email
    }

    # Отправляем тебе полную инфу
    await bot.send_message(
        ADMIN_ID,
        f"Новая регистрация!\n"
        f"ID: {user_id}\n"
        f"Имя: {name} {surname}\n"
        f"Адрес: {address}\n"
        f"Телефон: {phone}\n"
        f"Email: {email}"
    )

    await message.answer(
        f"Спасибо! Зарегистрировал:\n"
        f"Имя: {name} {surname}\n"
        f"Адрес: {address}\n"
        f"Телефон: {phone}\n"
        f"Email: {email}\n\n"
        "Теперь выбирай, что нужно:",
        reply_markup=menu_kb
    )
    await state.clear()

@dp.message(lambda m: m.text == "Проверить скорость")
async def speed_test(message: types.Message):
    await message.answer("Запускаю тест... подожди 10 секунд.")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
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
    await message.answer("Напиши адрес, где нет интернета:")
    await state.set_state(Form.outage_address)

@dp.message(Form.outage_address)
async def outage_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Что случилось?")
    await state.set_state(Form.outage_type)

@dp.message(Form.outage_type)
async def outage_type(message: types.Message, state: FSMContext):
    data = await state.get_data()
    address = data.get("address")
    problem = message.text

    user_id = message.from_user.id
    ud = user_data.get(user_id, {})  # если нет — пустой dict

    # Отправляем заявку
    await bot.send_message(
        ADMIN_ID,
        f"Сбой от {user_id}!\n"
        f"Имя: {ud.get('name', 'неизвестно')} {ud.get('surname', '')}\n"
        f"Адрес: {ud.get('address', 'неизвестно')}\n"
        f"Телефон: {ud.get('phone', 'неизвестно')}\n"
        f"Проблема: {problem}"
    )

    await message.answer("Сбой зафиксирован. Техник в пути. Спасибо!")
    await state.clear()

@dp.message(lambda m: m.text == "Мой баланс")
async def balance(message: types.Message):
    await message.answer("Баланс: 45.67 USD (на 23 марта 2026).")

@dp.message(lambda m: m.text == "Поддержка")
async def support_start(message: types.Message, state: FSMContext):
    await message.answer("Напиши вопрос:")
    await state.set_state(Form.support_message)

@dp.message(Form.support_message)
async def support_send(message: types.Message, state: FSMContext):
    question = message.text

    user_id = message.from_user.id
    ud = user_data.get(user_id, {})  # если нет — пустой

    await bot.send_message(
        ADMIN_ID,
        f"Поддержка от {user_id}!\n"
        f"Имя: {ud.get('name', 'неизвестно')} {ud.get('surname', '')}\n"
        f"Адрес: {ud.get('address', 'неизвестно')}\n"
        f"Телефон: {ud.get('phone', 'неизвестно')}\n"
        f"Вопрос: {question}"
    )

    await message.answer("Запрос отправлен. Ответят быстро.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
