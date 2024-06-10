from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message
from aiogram.filters import Command

from bot_commands import BotCommands
from const import Const


def __init__():
    r = Router()
    # r.message.filter(ChatTypeFilter(chat_type=[Const.GROUP, Const.SUPER_GROUP]))
    r.message.filter(F.chat.type.in_({Const.GROUP, Const.SUPER_GROUP}))
    return r


router = __init__()


@router.message(
    Command(commands=[BotCommands.DICE]),
)
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(
    Command(commands=[BotCommands.BASKETBALL]),
)
async def cmd_basketball_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)


@router.message(
    # ChatTypeFilter(chat_type=[Const.GROUP, Const.SUPER_GROUP]),
    Command(commands=[BotCommands.DICE]),
)
async def cmd_dice(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(
    # ChatTypeFilter(chat_type=[Const.GROUP, Const.SUPER_GROUP]),
    Command(commands=[BotCommands.BASKETBALL]),
)
async def cmd_basketball(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
