import asyncio
import logging

from config.config import init_bot_config


async def main() -> None:
    """Bots entry point."""
    main_bot, dp = init_bot_config()
    # skip all unprocessed updates. But why?
    await main_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(main_bot)


if __name__ == "__main__":
    logging.info("start polling messages")
    asyncio.run(main())
