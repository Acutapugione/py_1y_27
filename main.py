from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class StartCallback(CallbackData, prefix="start"):
    name: str
    age: int
    gender: bool


data_base_mock = [
    StartCallback(name="Дмитро", age=27, gender=True),
    StartCallback(name="Євгенія", age=27+18, gender=False),
    StartCallback(name="В'ячеслав", age=27-7, gender=True),
]
load_dotenv()


# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
# print(1, 2, 3, 4, 5, 6, )

@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    builder = InlineKeyboardBuilder()

    for data in data_base_mock:
        builder.button(
            text=f"{data.name}", 
            callback_data=data.pack() 
        )
    builder.adjust(3, 2, 3, 2) 

    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!", 
        reply_markup=builder.as_markup()
    )

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Чим можу допомогти?")

@dp.callback_query(StartCallback.filter())
async def callb_start(callback: CallbackQuery, callback_data: StartCallback) -> None:
    await callback.message.answer(text=f"{callback_data=}")

# @dp.message()
# async def echo(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender

#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


@dp.callback_query()
async def callb_query(callback: CallbackQuery) -> None:
    await callback.message.reply(text=f"{callback.data=}")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())