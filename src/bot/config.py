import logging

from datetime import datetime

from config_reader import get_config_reader
from const import Const
from commands.cmd_start import router as start_router
from commands.cmd_with_numbers import router as numeric_commands_router
from commands.cmd_extra import router as extra_commands_router
from commands.cmd_group_games import router as group_games_router
from commands.unprocessable_updates import router as unprocessed_commands_router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from middlewares.base import SomeOuterMiddleware


def init_bot_config() -> (Bot, Dispatcher):
    """Init tg bot and dispatcher instances."""
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
    # dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.update.outer_middleware(SomeOuterMiddleware())
    dp.include_routers(
        start_router,
        numeric_commands_router,
        extra_commands_router,
        group_games_router,
        unprocessed_commands_router,
    )
    dp[Const.BOT_CREATED_AT_LOWER] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp[Const.TELEGRAM_UID] = get_config_reader().tg_user_id

    return bot, dp
