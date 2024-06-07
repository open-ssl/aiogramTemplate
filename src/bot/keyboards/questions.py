from aiogram.types import ReplyKeyboardMarkup
from keyboards.main import KeyboardButtonConst, KeyboardGenerator


def get_yes_no_reply_markup_keyboard() -> ReplyKeyboardMarkup:
    """
    Generate reply keyboard with yes/no buttons
    """
    return KeyboardGenerator.generate_reply_keyboard(
        [KeyboardButtonConst.YES, KeyboardButtonConst.NO]
    )
