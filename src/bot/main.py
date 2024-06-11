import asyncio
import logging

from config.config import init_bot_config


async def main() -> None:
    """Bots entry point."""
    # skip all unprocessed updates. But why?
    await main_bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(main_bot)
    finally:
        await main_bot.session.close()


if __name__ == "__main__":
    main_bot, dp = init_bot_config()
    logging.info("start polling messages")
    asyncio.run(main())
