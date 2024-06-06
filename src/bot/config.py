import logging

from datetime import datetime
from config_reader import get_config_reader

from const import Const

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware


def init_bot_config() -> (Bot, Dispatcher):
    """Init tg bot and dispancher instances."""
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=get_config_reader().bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # same answer to all callbacks
    # show_alert = True is so noizy
    # dp.callback_query.middleware(CallbackAnswerMiddleware(
    #     pre=True, text="Ready!", show_alert=False
    # ))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp[Const.BOT_CREATED_AT_LOWER] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp[Const.TELEGRAM_UID] = get_config_reader().tg_user_id

    return bot, dp