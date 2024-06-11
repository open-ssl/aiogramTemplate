from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from fluent.runtime import FluentLocalization
from typing import Callable, Dict, Any, Awaitable
from random import randint


class SomeInnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        print("Before handler")
        result = await handler(event, data)
        print("After handler")
        # if no handler result was returned  - update is skipped/dropped
        return result


class LocaleMiddleware(BaseMiddleware):
    def __init__(
        self,
        locales_data: Dict[str, FluentLocalization],
    ):
        self.locales_data = locales_data

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["locales"] = self.locales_data
        return await handler(event, data)


def get_internal_id(user_id: int) -> int:
    return randint(1, 100) + user_id


class SomeOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        data["internal_id"] = get_internal_id(user.id)
        return await handler(event, data)
