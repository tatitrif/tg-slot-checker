"""Модуль для выполнения шагов сценария бронирования."""

import asyncio
import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)


class StepExecutor:
    """Выполняет шаги сценария."""

    def __init__(self, client, target_entity, booking_data: dict[str, str]):
        """
        Инициализирует исполнитель шагов.

        Args:
            client: Клиент Telegram
            target_entity: Целевой entity (бот)
            booking_data: Словарь для хранения данных бронирования
        """
        self.client = client
        self.target = target_entity
        self.booking_data = booking_data

    async def execute_steps(
        self, steps: list[tuple[Callable, str | None]], step_delay: int
    ) -> bool:
        """Последовательно выполняет шаги."""
        for step_func, expected_data in steps:
            success = await step_func()
            if not success:
                return False

            if expected_data and expected_data in self.booking_data:
                logger.debug(
                    "Сохранили %s: %s", expected_data, self.booking_data[expected_data]
                )

            await asyncio.sleep(step_delay)

        return True
