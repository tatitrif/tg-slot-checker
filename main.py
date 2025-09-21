"""Основной модуль для запуска приложения бронирования слотов."""

import asyncio
import logging
from asyncio import exceptions

from bot.checker import CheckerSlotBot

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Главная функция запуска."""
    try:
        bot = CheckerSlotBot()
        success = await bot.start()
        logger.info("Программа завершена %s", "успешно" if success else "с ошибками")
    except exceptions.CancelledError:
        logger.info("Программа прервана пользователем")
    except Exception as e:
        logger.error("Непредвиденная ошибка: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
