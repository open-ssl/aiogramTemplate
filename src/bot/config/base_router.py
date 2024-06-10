from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from typing import Any


class BaseRouter(Router):
    message_instance: Message = None

    def receive_message(self, *args: Any, **kwargs: Any):
        def _receive_message(*i_args: Any, **i_kwargs: Any):
            msg = None

            for item in args:
                if isinstance(item, Message):
                    msg = item

            self.message_instance = msg
            return

        return _receive_message

    def message_answer(self, text: str, reply_markup=None):
        if not self.message_instance:
            return

        if not reply_markup:
            reply_markup = ReplyKeyboardRemove()

        return self.message_instance.answer(text=text, reply_markup=reply_markup)
