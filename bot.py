from aiogram import Bot, Dispatcher
import asyncio

bot = Bot(token='8694337840:AAGPruuIzE5zfrh5fmiQxfR0w03-RQT_D7g')
dp = Dispatcher()

@dp.message()
async def echo(message):
    await message.answer("Привет, я живой!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
