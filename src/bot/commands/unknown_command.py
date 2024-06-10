from aiogram import Router, F
from aiogram.types import Message

from answers.const import AnswerConst


def __init__():
    return Router()


router = __init__()


@router.message(F.sticker)
async def message_with_sticker(message: Message):
    """sendMessage with sticker handler."""

    await message.answer(AnswerConst.STICKER)


@router.message(F.animation)
async def message_with_animation(message: Message):
    """sendMessage with animation handler."""

    await message.answer(AnswerConst.ANIMATION)
