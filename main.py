"""Основной модуль для запуска приложения бронирования слотов."""

import asyncio
import logging
from bot.checker import CheckerSlotBot

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


async def main():
    """Точка входа: запускает CheckerSlotBot."""
    bot = CheckerSlotBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
