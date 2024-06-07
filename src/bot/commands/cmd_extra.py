from aiogram import F, Router, html, types, Bot, flags
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.callback_answer import CallbackAnswer
from contextlib import suppress
from magic_filter import F as MagicFilter
from typing import AnyStr, Optional

from bot_commands import BotCommands
from callbacks import NumbersCallbackFactory
from const import Const, CallbackConst
from keyboards.main import KeyboardGenerator, get_switch_keyboard, get_keyboard_fab
from random import randint


def __init__():
    return Router()


router = __init__()


@router.message(Command(BotCommands.ANSWER))
async def cmd_answer(message: types.Message):
    await message.answer("Simple answer")


# Example: data in command handler
# Command: /reply
####################################################################################
@router.message(Command(BotCommands.REPLY))
async def cmd_reply(message: types.Message, bot_created_at: AnyStr):
    await message.reply(
        "Reply answer that informs about start bot time. It's %s" % bot_created_at
    )


####################################################################################


# Example: parse mode
# Command: /parsed
####################################################################################
@router.message(F.text, Command(BotCommands.PARSED))
async def cmd_parsed(message: types.Message):
    await message.answer("HTML mode: Hello, <b>world</b>!", parse_mode=ParseMode.HTML)
    await message.answer(
        "MARKDOWNV2 mode: Hello, *world*\!", parse_mode=ParseMode.MARKDOWN_V2
    )
    await message.answer("None mode: Hello, world!", parse_mode=None)


@router.message(F.text, Command(BotCommands.HELLO))
async def cmd_hello(message: types.Message):
    # shielded input
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
        parse_mode=ParseMode.HTML,
    )


####################################################################################


# Example: input data
# Command: /extract_data
# /extract_data text@text.text
####################################################################################
@router.message(F.text, Command(BotCommands.EXTRACT_DATA))
async def cmd_extract_data(message: types.Message):
    data = {"url": "<N/A>", "email": "<N/A>", "code": "<N/A>"}
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            # Incorrect
            # data[item.type] = message.text[item.offset : item.offset+item.length]
            # Correct
            data[item.type] = item.extract_from(message.text)
    await message.reply(
        "So what I found:\n"
        f"URL: {html.quote(data.get('url'))}\n"
        f"E-mail: {html.quote(data.get('email'))}\n"
        f"Password: {html.quote(data.get('code'))}"
    )


####################################################################################


# Example: cmd with extra text.
# Command: /command_with_text, Sample: {/command_with_text 20h This is delayed}
####################################################################################
@router.message(Command(BotCommands.COMMAND_WITH_TEXT))
async def cmd_command_with_text(message: types.Message, command: CommandObject):
    # If args are not provided command.args will be None
    if command.args is None:
        await message.answer("Error: args are not provided")
        return
    # correct sample: {/command_with_args 20h This is delayed}

    # split args for two parts by first space
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    # if less than two parts are received you will get a ValueError
    except ValueError:
        await message.answer(
            "Error: Wrong command format. Example:\n"
            "/command_with_args {time} {message}"
        )
        return
    await message.answer(
        "Timer added!\n" f"Time: {delay_time}\n" f"Text: {text_to_send}"
    )


####################################################################################


# Example: 4x4 reply keyboard
# Command: /reply_builder
####################################################################################
@router.message(Command(BotCommands.REPLY_BUILDER))
async def reply_builder(message: types.Message):
    keyboard_buttons = list()
    for i in range(1, 17):
        keyboard_buttons.append(str(i))

    await message.answer(
        "Choice number:",
        reply_markup=KeyboardGenerator.generate_reply_builder_keyboard(
            keyboard_buttons, 4
        ),
    )


####################################################################################


# Example: Inline Keyboard generating
# Command: /reply_inline
####################################################################################
@router.message(Command(BotCommands.REPLY_INLINE))
async def cmd_reply_url(message: types.Message, bot: Bot, telegram_uid: int):
    keyboard_buttons = list()
    # builder = InlineKeyboardBuilder()
    keyboard_buttons.append(
        types.InlineKeyboardButton(text=Const.GITHUB, url="https://github.com")
    )
    keyboard_buttons.append(
        types.InlineKeyboardButton(
            text=Const.TELEGRAM, url="tg://resolve?domain=telegram"
        )
    )

    # to show id-btn, user's flag has_private_forwards must be False
    chat_info = await bot.get_chat(telegram_uid)
    if not chat_info.has_private_forwards:
        keyboard_buttons.append(
            types.InlineKeyboardButton(
                text=Const.SOME_USER, url=f"tg://user?id={telegram_uid}"
            )
        )

    await message.answer(
        Const.CHOICE_LINK,
        reply_markup=KeyboardGenerator.generate_inline_markup_keyboard(
            buttons=keyboard_buttons
        ),
    )


####################################################################################


# Example: callback query with some instant message in frame
# Command: /random
####################################################################################
@router.message(Command(BotCommands.RANDOM))
async def cmd_random(message: types.Message):
    keyboard_schema = dict({Const.PRESS_ME: CallbackConst.RANDOM_VALUE})

    await message.answer(
        "Press the button to bot send number from 1 to 10",
        reply_markup=KeyboardGenerator.generate_inline_markup_keyboard_with_callback(
            keyboard_schema
        ),
    )


@router.callback_query(F.data == CallbackConst.RANDOM_VALUE)
async def send_random_value(callback: types.CallbackQuery):
    """Send random value to user on click 'Send me random value'."""
    await callback.message.answer(f"Generated number - {str(randint(1, 10))}")
    await callback.answer(text="Some instant message with info!", show_alert=True)


# Example: callback query with process callback text and save data in memory
# Command: /numbers
####################################################################################


saved_user_data_in_memory = dict()


# Example: ignore a telegram api error
async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"{Const.SET_NUMBER}: {new_value}", reply_markup=get_switch_keyboard()
        )


@router.message(Command(BotCommands.NUMBERS))
async def cmd_numbers(message: types.Message):
    saved_user_data_in_memory[message.from_user.id] = 0
    await message.answer(f"{Const.SET_NUMBER}: 0", reply_markup=get_switch_keyboard())


@router.callback_query(F.data.startswith(BotCommands.NUM_PREFIX))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = saved_user_data_in_memory.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == Const.INCR:
        saved_user_data_in_memory[callback.from_user.id] = user_value + 1
        await update_num_text(callback.message, user_value + 1)
    elif action == Const.DECR:
        saved_user_data_in_memory[callback.from_user.id] = user_value - 1
        await update_num_text(callback.message, user_value - 1)
    elif action == Const.FINISH:
        await callback.message.edit_text(f"{Const.TOTAL}: {user_value}")

    await callback.answer()


####################################################################################


# Example: process all callbacks text with prefix with separate commands
####################################################################################


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"{Const.SET_NUMBER}: {new_value}", reply_markup=get_keyboard_fab()
        )


@router.message(Command(BotCommands.NUMBERS_FAB))
async def cmd_numbers_fab(message: types.Message):
    saved_user_data_in_memory[message.from_user.id] = 0
    await message.answer(f"{Const.SET_NUMBER}: 0", reply_markup=get_keyboard_fab())


# Pressed one of the buttons: -2, -1, +1, +2
@router.callback_query(
    NumbersCallbackFactory.filter(MagicFilter.action == Const.CHANGE)
)
@flags.callback_answer(pre=False)
async def callbacks_num_change_fab(
    callback: types.CallbackQuery,
    callback_answer: CallbackAnswer,
    callback_data: NumbersCallbackFactory,
):
    # Current number value
    user_value = saved_user_data_in_memory.get(callback.from_user.id, 0)

    new_value = user_value + callback_data.value

    # we can define custom logic
    if new_value > 0:
        callback_answer.text = "More than 0!"
    elif new_value == 0:
        callback_answer.text = "Is 0!"
    else:
        callback_answer.text = "Less than 0!"
        callback_answer.cache_time = 3

    saved_user_data_in_memory[callback.from_user.id] = new_value
    await update_num_text_fab(callback.message, new_value)
    await callback.answer()


# Press "Apply" button
@router.callback_query(
    NumbersCallbackFactory.filter(MagicFilter.action == Const.FINISH)
)
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    # Current value
    user_value = saved_user_data_in_memory.get(callback.from_user.id, 0)

    await callback.message.edit_text(f"{Const.TOTAL}: {user_value}")
    await callback.answer()


####################################################################################
