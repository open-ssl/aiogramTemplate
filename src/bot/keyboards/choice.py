from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.main import KeyboardButtonConst, KeyboardGenerator


def get_left_right_btn_reply_markup_keyboard() -> ReplyKeyboardMarkup:
    """
    Generate reply keyboard with left/right buttons
    """
    buttons = [
        [KeyboardButton(text=KeyboardButtonConst.LEFT_BUTTON)],
        [KeyboardButton(text=KeyboardButtonConst.RIGHT_BUTTON)],
    ]
    return KeyboardGenerator.generate_rows_reply_markup_keyboard(
        buttons, input_field_placeholder_text="Write some text here"
    )
