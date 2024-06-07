from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot_commands import BotCommands


def __init__():
    return Router()


router = __init__()


# Example: reply message
# Commands: /command1 || /command2 || /answer
####################################################################################


@router.message(Command(BotCommands.COMMAND1))
async def cmd_command1(message: Message):
    await message.reply("Text for Command 1")


@router.message(Command(BotCommands.COMMAND2))
async def cmd_command2(message: Message):
    await message.reply("Text for Command 2")


####################################################################################
