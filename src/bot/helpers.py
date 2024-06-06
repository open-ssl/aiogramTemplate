from aiogram import types
from const import Const


def get_switch_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
        ],
        [types.InlineKeyboardButton(text=Const.APPLY, callback_data="num_finish")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
