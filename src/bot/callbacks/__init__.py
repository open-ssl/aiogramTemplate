from aiogram.filters.callback_data import CallbackData
from typing import Optional


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None
