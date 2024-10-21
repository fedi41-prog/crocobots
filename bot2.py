from aiogram import Bot, Dispatcher, types, executor

bot = Bot('6687729977:AAHVq5Z0l9PRYIF_gDQJHq63pfxe-NUGvPs')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # await bot.send_message(message.chat.id, 'Hello')
    await message.answer('Hello')

executor.start_polling(dp)