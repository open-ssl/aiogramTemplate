import logging

from datetime import datetime

from config.config_reader import get_config_reader
from const import Const
from commands import (
    cmd_start,
    cmd_with_numbers,
    cmd_extra,
    cmd_group_games,
    cmd_fsm_food,
    unknown_command,
)
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from middlewares.base import SomeOuterMiddleware


def init_bot_config() -> (Bot, Dispatcher):
    """Init tg bot and dispatcher instances."""
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=get_config_reader().bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

    # same answer to all callbacks
    # show_alert = True is so noizy
    # dp.callback_query.middleware(CallbackAnswerMiddleware(
    #     pre=True, text="Ready!", show_alert=False
    # ))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    # dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.update.outer_middleware(SomeOuterMiddleware())
    dp.include_routers(
        cmd_start.router,
        cmd_with_numbers.router,
        cmd_extra.router,
        cmd_group_games.router,
        cmd_fsm_food.router,
        unknown_command.router,
    )
    dp[Const.BOT_CREATED_AT_LOWER] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp[Const.TELEGRAM_UID] = get_config_reader().tg_user_id

    return bot, dp
