import asyncio
import logging

from config.config import init_bot_config
from keyboards.main import KeyboardButtonConst

from aiogram import F, types

main_bot, dp = init_bot_config()


@dp.message(F.text.lower() == KeyboardButtonConst.LEFT_BUTTON.lower())
async def left_button_handler(message: types.Message):
    await message.reply(
        f"You choice {KeyboardButtonConst.LEFT_BUTTON}. It's okay",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@dp.message(F.text.lower() == KeyboardButtonConst.RIGHT_BUTTON.lower())
async def right_button_handler(message: types.Message):
    await message.reply(
        f"You choice {KeyboardButtonConst.RIGHT_BUTTON}. It's normal",
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def main() -> None:
    """Bots entry point."""
    # skip all unprocessed updates. But why?
    await main_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(main_bot)


if __name__ == "__main__":
    logging.info("start polling messages")
    asyncio.run(main())
