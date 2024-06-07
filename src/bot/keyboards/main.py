from functools import partial
from typing import Dict, List, Any, Optional

from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from const import Const
from callbacks import NumbersCallbackFactory


class KeyboardButtonConst:
    LEFT_BUTTON = "Left button"
    RIGHT_BUTTON = "Right button"

    YES = "Yes"
    NO = "No"


class KeyboardGenerator:
    @classmethod
    def generate_reply_builder_keyboard(
        cls, buttons: list[str], keyboard_size: int, with_resize_keyboard=True
    ) -> ReplyKeyboardMarkup:
        return cls._generate_reply_builder_keyboard(
            buttons, keyboard_size, with_resize_keyboard
        )

    @classmethod
    def generate_reply_keyboard(
        cls,
        buttons: list[str],
        input_field_placeholder_text="",
        with_resize_keyboard=True,
    ) -> ReplyKeyboardMarkup:
        return cls._generate_reply_keyboard(
            buttons, input_field_placeholder_text, with_resize_keyboard
        )

    @classmethod
    def generate_rows_reply_markup_keyboard(
        cls,
        buttons: list[str],
        input_field_placeholder_text="",
        with_resize_keyboard=True,
    ) -> ReplyKeyboardMarkup:
        return cls._generate_rows_reply_markup_keyboard(
            buttons, input_field_placeholder_text, with_resize_keyboard
        )

    @classmethod
    def generate_inline_markup_keyboard_with_url(
        cls, keyboard_schema: Dict[str, str]
    ) -> InlineKeyboardMarkup:
        return cls._generate_inline_markup_keyboard_with_url(keyboard_schema)

    @classmethod
    def generate_inline_markup_keyboard_with_callback(
        cls, keyboard_schema: Dict[str, str]
    ) -> InlineKeyboardMarkup:
        return cls._generate_inline_markup_keyboard_with_callback(keyboard_schema)

    @classmethod
    def generate_inline_markup_keyboard(
        cls, buttons: List[Any]
    ) -> InlineKeyboardMarkup:
        return cls._generate_inline_markup_keyboard(buttons)

    @staticmethod
    def _generate_reply_builder_keyboard(
        buttons: List[str], keyboard_size: int, with_resize_keyboard=True
    ) -> ReplyKeyboardMarkup:
        """Implementation of generating ReplyMarkupKeyboard by builder."""
        builder = ReplyKeyboardBuilder()
        for button_text in buttons:
            builder.add(KeyboardButton(text=button_text))

        builder.adjust(keyboard_size)
        return builder.as_markup(resize_keyboard=with_resize_keyboard)

    @staticmethod
    def _generate_reply_keyboard(
        buttons: List, input_field_placeholder_text: str, with_resize_keyboard: bool
    ) -> ReplyKeyboardMarkup:
        """Implementation of generating ReplyMarkupKeyboard."""
        keyboard = ReplyKeyboardBuilder()
        for button_text in buttons:
            keyboard.button(text=button_text)

        keyboard.adjust(len(buttons))

        reply_keyboard = keyboard.as_markup(resize_keyboard=with_resize_keyboard)

        if input_field_placeholder_text:
            reply_keyboard.input_field_placeholder = input_field_placeholder_text

        return reply_keyboard

    @staticmethod
    def _generate_rows_reply_markup_keyboard(
        buttons: List, input_field_placeholder_text: str, with_resize_keyboard: bool
    ) -> ReplyKeyboardMarkup:
        """Implementation of generating ReplyMarkupKeyboard with rows."""
        reply_keyboard = partial(
            ReplyKeyboardMarkup, keyboard=buttons, resize_keyboard=with_resize_keyboard
        )

        if input_field_placeholder_text:
            reply_keyboard.keywords["input_field_placeholder"] = (
                input_field_placeholder_text
            )

        return reply_keyboard()

    @staticmethod
    def _generate_inline_markup_keyboard(
        buttons: List[InlineKeyboardButton],
    ) -> InlineKeyboardMarkup:
        """Implementation of generating InlineMarkupKeyboard."""
        builder = InlineKeyboardBuilder()

        for button_data in buttons:
            builder.row(button_data)

        return builder.as_markup()

    @staticmethod
    def _generate_inline_markup_keyboard_with_url(
        keyboard_schema: Dict[str, str]
    ) -> InlineKeyboardMarkup:
        """Implementation of generating InlineMarkupKeyboard with url"""
        builder = InlineKeyboardBuilder()

        for keyboard_text, keyboard_url in keyboard_schema.items():
            builder.add(InlineKeyboardButton(text=keyboard_text, url=keyboard_url))

        return builder.as_markup()

    @staticmethod
    def _generate_inline_markup_keyboard_with_callback(
        keyboard_schema: Dict[str, str]
    ) -> InlineKeyboardMarkup:
        """Implementation of generating InlineMarkupKeyboard with callback_data"""
        builder = InlineKeyboardBuilder()

        for keyboard_text, keyboard_callback_data in keyboard_schema.items():
            builder.add(
                InlineKeyboardButton(
                    text=keyboard_text, callback_data=keyboard_callback_data
                )
            )

        return builder.as_markup()


def get_switch_keyboard():
    """Generate switch keyboard"""
    buttons = [
        [
            InlineKeyboardButton(text="-1", callback_data="num_decr"),
            InlineKeyboardButton(text="+1", callback_data="num_incr"),
        ],
        [InlineKeyboardButton(text=Const.APPLY, callback_data="num_finish")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="-2", callback_data=NumbersCallbackFactory(action=Const.CHANGE, value=-2)
    )
    builder.button(
        text="-1", callback_data=NumbersCallbackFactory(action=Const.CHANGE, value=-1)
    )
    builder.button(
        text="+1", callback_data=NumbersCallbackFactory(action=Const.CHANGE, value=1)
    )
    builder.button(
        text="+2", callback_data=NumbersCallbackFactory(action=Const.CHANGE, value=2)
    )
    builder.button(
        text=Const.APPLY, callback_data=NumbersCallbackFactory(action=Const.FINISH)
    )
    builder.adjust(4)
    return builder.as_markup()
