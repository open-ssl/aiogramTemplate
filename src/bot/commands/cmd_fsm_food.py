from aiogram import F

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from bot_commands import BotCommands
from config.base_router import BaseRouter
from keyboards.main import KeyboardGenerator


def __init__():
    return BaseRouter()


router = __init__()


class CmdFoodData:
    available_food_names = ["Sushi", "Pasta", "Pizza"]
    available_food_sizes = ["Small", "Medium", "Big"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


@router.message(StateFilter(None), Command(BotCommands.FOOD))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Select the food:",
        reply_markup=KeyboardGenerator.generate_one_row_reply_markup_keyboard(CmdFoodData.available_food_names)
    )
    # Set state "choosing food name"
    await state.set_state(OrderFood.choosing_food_name)


@router.message(
    OrderFood.choosing_food_name,
    F.text.in_(CmdFoodData.available_food_names)
)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Thank you. Now, choose meal size, please:",
        reply_markup=KeyboardGenerator.generate_one_row_reply_markup_keyboard(CmdFoodData.available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)


# handler for all different texts (pollute tg updates)
@router.message(OrderFood.choosing_food_name)
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know such food.\n\n"
             "Choose one of the meal from the given list, please:",
        reply_markup=KeyboardGenerator.generate_one_row_reply_markup_keyboard(CmdFoodData.available_food_names)
    )


@router.message(OrderFood.choosing_food_size, F.text.in_(CmdFoodData.available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(text=f"You've been chosen {message.text.lower()} size: {user_data['chosen_food']}.\n"
                              f"Let's try to order drinks with /drinks command")

    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know such meal size.\n\n""Choose one of the variants from the given list, please:",
        reply_markup=KeyboardGenerator.generate_one_row_reply_markup_keyboard(CmdFoodData.available_food_sizes)
    )


# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "cancel")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Nothing to cancel",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Action has canceled",
        reply_markup=ReplyKeyboardRemove()
    )
