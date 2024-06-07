import re

from aiogram import Router, F
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from answers.const import AnswerConst
from bot_commands import BotCommands
from keyboards.questions import get_yes_no_reply_markup_keyboard
from keyboards.main import KeyboardButtonConst


def __init__():
    return Router()


router = __init__()


# Example: Deep link as a start parameter
# Command: /start  Sample {/start=link_245}
####################################################################################
@router.message(
    Command(BotCommands.START),
    CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r"link_(\d+)"))),
)
async def cmd_start_book(message: Message, command: CommandObject):
    link_number = command.args.split("_")[1]
    await message.answer(f"Sending link №{link_number}")


####################################################################################


# Start Version 1
@router.message(Command(BotCommands.START))
async def cmd_start(message: Message):
    await message.answer(
        AnswerConst.ARE_YOU_SATISFIED, reply_markup=get_yes_no_reply_markup_keyboard()
    )


@router.message(F.text.lower() == KeyboardButtonConst.YES.lower())
async def answer_yes(message: Message):
    await message.answer(AnswerConst.WELL, reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == KeyboardButtonConst.NO.lower())
async def answer_no(message: Message):
    await message.answer(AnswerConst.PITY, reply_markup=ReplyKeyboardRemove())


# Start Version 2
# ####################################################################################

# from keyboards.choice import get_left_right_btn_reply_markup_keyboard


# @router.message(Command(BotCommands.START))
# async def cmd_start(message: Message) -> None:
#     await message.answer("Choice button position", reply_markup=get_left_right_btn_reply_markup_keyboard())


# ####################################################################################
